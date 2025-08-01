from fastapi import FastAPI, HTTPException, Request
from data_center import salva_su_supabase, cerca_analisi_simili
from pydantic import BaseModel
from modulo_filtra_bandi import filtra_bandi
from scoring_bandi import calcola_scoring_bandi
import pandas as pd
import requests
import logging
import asyncio
from typing import List, Dict
from calendar_api import router as calendar_router
from prompt_evoluto import master_flow
from template_pof import ISTRUZIONI_HTML
from pathlib import Path
import os
from evoluto_capitaleaziendale_it__jit_plugin import getFasePrompt as get_fase_prompt
from datetime import datetime
from supabase import create_client
# ⬇️ Caricamento checklist_fasi.json
import json

with open("checklist_fasi.json", "r") as f:
    CHECKLIST = json.load(f)

# 🔁 Variabile globale temporanea per uso interno nelle fasi
analisi_corrente = {
    "utile_netto": None
}

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Inizializza FastAPI
app = FastAPI()

app.include_router(calendar_router, prefix="/calendar")

# 🔗 URL del JSON dei bandi su GitHub
JSON_URL = "https://raw.githubusercontent.com/eVoluto25/evoluto_app/refs/heads/main/opendata-export.json"

# 🧾 Modello input principale per la prima chiamata (filtra-bandi)
class AziendaInput(BaseModel):
    dimensione: str                 # Es: "Piccola Impresa"
    regione: str                    # Es: "Lazio"
    mcc_rating: str                 # Es: "BBB"
    z_score: float                  # Es: 1.8
    numero_dipendenti: int          # Es: 8
    ebitda: float                   # Es: 249121
    utile_netto: float              # Es: 124128
    fatturato: float                # Es: 925439
    obiettivo_preferenziale: str    # Es: "Digitalizzazione"

# 🧾 Modelli input per la seconda chiamata (scoring-bandi)
class BandoInput(BaseModel):
    Titolo_Bando: str
    Data_Scadenza: str
    Obiettivo_Bando: List[str]
    Prioritario_SI_NO: str
    Percentuale_Spesa: float
    Tipo_Agevolazione: str
    Costi_Ammessi: str
    Descrizione_Sintetica: str

class AziendaScoringInput(BaseModel):
    regione: str
    ebitda: float
    utile_netto: float
    fatturato: float

class ScoringInput(BaseModel):
    azienda: AziendaScoringInput
    bandi: List[BandoInput]

class AnalisiAziendaInput(BaseModel):
    ateco: str
    regione: str
    dimensione: str
    forma_giuridica: str
    fatturato: float
    ebitda: float
    utile_netto: float
    patrimonio_netto: float
    dipendenti: int
    mcc_rating: str
    z_score: float
    obiettivo_azienda: str
    bandi_trovati: int
    probabilita_media_approvazione: float

class ChecklistRequest(BaseModel):
    fase_id: str
    task_completati: List[str]

def aggiorna_log_giornaliero():
    oggi = str(date.today())
    try:
        res = supabase.table("gpt_evoluto_giornaliero").select("*").eq("data", oggi).execute()
        if res.data:
            supabase.table("gpt_evoluto_giornaliero").update({
                "conteggio": res.data[0]["conteggio"] + 1
            }).eq("data", oggi).execute()
        else:
            supabase.table("gpt_evoluto_giornaliero").insert({
                "data": oggi,
                "conteggio": 1
            }).execute()
    except Exception as e:
        logger.warning(f"⚠️ Errore logging giornaliero Supabase: {str(e)}")

@app.post("/filtra-bandi")
async def filtra_bandi_per_azienda(input_data: AziendaInput):
    logger.info("📡 Entrata nella funzione filtra_bandi_per_azienda")
    aggiorna_log_giornaliero()
    logger.info(f"✅ Contenuto input_data ricevuto: {input_data}")
    logger.info(f"📋 input_data.dict(): {input_data.dict()}")
    logger.info(f"🔍 numero_dipendenti: {input_data.numero_dipendenti}")
    logger.info(f"🔍 ebitda: {input_data.ebitda}")
    logger.info(f"🔍 utile_netto: {input_data.utile_netto}")
    logger.info(f"🔍 fatturato: {input_data.fatturato}")

    try:
        logger.info(f"✅ Ricevuti dati da eVoluto: {input_data.dict()}")

        # 🔄 Carica i dati JSON dei bandi
        logger.info(f"📲 Scarico il JSON da: {JSON_URL}")
        response = requests.get(JSON_URL)
        if response.status_code != 200:
            logger.error(f"❌ Errore nel download del JSON: {response.status_code}")
            raise HTTPException(status_code=500, detail="Errore nel recupero dati JSON")

        dati_json = response.json()
        if isinstance(dati_json, dict):
            dati_json = [dati_json]

        # ✅ Crea DataFrame
        df = pd.DataFrame(dati_json)
        logger.info(f"✅ DataFrame creato: {df.shape[0]} righe, {df.shape[1]} colonne")
        logger.info(f"🔍 Colonne presenti nel DataFrame: {df.columns.tolist()}")

        if df.empty:
            return {"bandi": [], "messaggio": "Nessun bando disponibile"}

        # ✅ Filtra i bandi
        bandi_filtrati = filtra_bandi(
            df=df,
            regione=input_data.regione,
            dimensione=input_data.dimensione,
            obiettivo_preferenziale=input_data.obiettivo_preferenziale,
            mcc_rating=input_data.mcc_rating,
            z_score=input_data.z_score,
            numero_dipendenti=input_data.numero_dipendenti,
            ebitda=input_data.ebitda,
            utile_netto=input_data.utile_netto,
            fatturato=input_data.fatturato,
            max_results=20
        )

        if not bandi_filtrati:
            return {"bandi": [], "messaggio": "Nessun bando compatibile trovato"}

        # 🔍 Controllo e integrazione campi obbligatori prima dello scoring
        for bando in bandi_filtrati:
            if not bando.get("Titolo Bando"):
                bando["Titolo Bando"] = "Titolo non disponibile"
            if not bando.get("Data Scadenza"):
                bando["Data Scadenza"] = "31/12/2025"
            if not bando.get("Obiettivo Bando") or not isinstance(bando.get("Obiettivo Bando"), list):
                bando["Obiettivo Bando"] = ["Digitalizzazione"]
            if not bando.get("Prioritario SI/NO") or bando["Prioritario SI/NO"] not in ["SI", "NO"]:
                bando["Prioritario SI/NO"] = "NO"
            if "Percentuale Spesa" not in bando:
                bando["Percentuale Spesa"] = None
            if not bando.get("Tipo Agevolazione"):
                bando["Tipo Agevolazione"] = "Contributo/Fondo perduto"
            if not bando.get("Costi Ammessi"):
                bando["Costi Ammessi"] = "Dato non disponibile"
            if not bando.get("Descrizione Sintetica"):
                bando["Descrizione Sintetica"] = "Dato non disponibile"

        # 🔄 Rinomina i campi in formato compatibile con lo YAML (underscore)
        bandi_compatibili = []
        for bando in bandi_filtrati:
            bando_normalizzato = {k.replace(" ", "_"): v for k, v in bando.items()}
            bando_corretto = {
                "Titolo_Bando": bando_normalizzato.get("Titolo_Bando"),
                "Data_Scadenza": bando_normalizzato.get("Data_Scadenza"),
                "Obiettivo_Bando": bando_normalizzato.get("Obiettivo_Bando"),
                "Prioritario_SI_NO": bando_normalizzato.get("Prioritario_SI_NO"),
                "Percentuale_Spesa": bando_normalizzato.get("Percentuale_Spesa"),
                "Tipo_Agevolazione": bando_normalizzato.get("Tipo_Agevolazione"),
                "Costi_Ammessi": bando_normalizzato.get("Costi_Ammessi"),
                "Descrizione_Sintetica": bando_normalizzato.get("Descrizione_Sintetica"),
        }
        bandi_compatibili.append(bando_corretto)

        # ✅ Calcola scoring finale
        bandi_finali = calcola_scoring_bandi(
            bandi=bandi_filtrati,
            azienda={
                "regione": input_data.regione,
                "ebitda": input_data.ebitda,
                "utile_netto": input_data.utile_netto,
                "fatturato": input_data.fatturato
            },
        )

        # ✅ Restituisci lista finale
        return {
            "bandi": bandi_finali,
            "totale": len(bandi_finali)
        }

    except Exception as e:
        logger.error(f"❌ Errore generale: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scoring-bandi")
async def scoring_bandi(input_data: ScoringInput):
    logger.info("📡 Entrata nella funzione scoring_bandi")
    logger.info(f"✅ Contenuto input_data ricevuto: {input_data}")

    try:
        # ✅ Calcola scoring finale
        bandi_finali = calcola_scoring_bandi(
            bandi=[b.dict() for b in input_data.bandi],
            azienda={
                "regione": input_data.azienda.regione,
                "ebitda": input_data.azienda.ebitda,
                "utile_netto": input_data.azienda.utile_netto,
                "fatturato": input_data.azienda.fatturato
            },
        )

        return {
            "bandi": bandi_finali,
            "totale": len(bandi_finali)
        }

    except Exception as e:
        logger.error(f"❌ Errore nella funzione scoring_bandi: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

from prompt_evoluto import master_flow  

@app.get("/get-fase/{fase_id}")
async def get_fase(fase_id: str):
    logger.info(f"📥 Richiesta ricevuta per fase: {fase_id}")

    if fase_id not in master_flow:
        raise HTTPException(status_code=404, detail="Fase non trovata")

    if fase_id == "fase_0":
        return {
            "fase": master_flow[fase_id]
        }

    # ⬇️ Carica checklist per la fase
    task_richiesti = CHECKLIST.get(fase_id, {}).get("checklist", [])

    # ⬇️ Esegui verifica checklist
    if task_richiesti:
        logger.info(f"🧪 Verifica checklist per {fase_id}")
        risultato = await recupera_fase_con_verifica(fase_id, task_richiesti)

        if "errore" in risultato:
            return risultato

        return {
            "fase": risultato["fase"],
            "istruzioni_html": ISTRUZIONI_HTML
        }

    # ⬇️ Se non ci sono task associati
    return {
        "fase": master_flow[fase_id],
        "istruzioni_html": ISTRUZIONI_HTML
    }
    
@app.post("/analizza-azienda")
async def analizza_azienda(input_data: AnalisiAziendaInput):
    logger.info("📡 Entrata nella funzione analizza_azienda (FASE 6)")
    try:
        # ➕ Completa con data analisi
        data_dict = input_data.dict(exclude_unset=True)
        data_dict["data_analisi"] = date.today().isoformat()

        # ✅ Salva su Supabase
        salva_su_supabase(data_dict)

        # 🔍 Verifica aziende simili
        risultato_benchmark = cerca_analisi_simili(data_dict)

        return {
            "messaggio": risultato_benchmark.get("messaggio", "Nessun messaggio disponibile"),
            "compatibilita_media": risultato_benchmark.get("compatibilita_media", 0),
            "analisi_simili_trovate": risultato_benchmark.get("analisi_simili_trovate", [])
        }

    except Exception as e:
        logger.error(f"❌ Errore nella funzione analizza_azienda: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verifica_checklist_fase")
async def verifica_checklist_fase(payload: ChecklistRequest):
    logger.info("✅ Verifica checkList fase_id=%s | task_completati=%s", payload.fase_id, [str(x) for x in payload.task_completati])

    richiesti = CHECKLIST.get(payload.fase_id, {}).get("checklist", [])
    mancanti = [x for x in richiesti if x not in payload.task_completati]

    if mancanti:
        logger.warning(f"❌ Fase {payload.fase_id} incompleta. Task mancanti: {mancanti}")
        raise HTTPException(
            status_code=400,
            detail={
                "fase_incompleta": payload.fase_id,
                "task_mancanti": mancanti,
                "status": "errore",
                "timestamp": datetime.now().isoformat()
            }
        )

    logger.info(f"✅ Fase {payload.fase_id} completata correttamente.")
    return {
        "fase_completata": payload.fase_id,
        "task_completati": payload.task_completati,
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }

async def recupera_fase_con_verifica(fase_id: str, task_completati: list[str]):
    payload = ChecklistRequest(fase_id=fase_id, task_completati=task_completati)

    try:
        await verifica_checklist_fase(payload)
    except HTTPException as e:
        logger.error(f"❌ Errore checklist: {e.detail}")
        return {
            "errore": "Checklist incompleta",
            "dettagli": e.detail
        }

    # ✅ Recupera fase da API ufficiale
    loop = asyncio.get_event_loop()
    risposta = await loop.run_in_executor(None, get_fase_prompt, fase_id)


    # 🔔 Notifica automatica
    notifica_fase_completata(fase_id, utente_id="admin")
    
    return risposta

@app.post("/notifica_fase")
async def notifica_fase(request: Request):
    try:
        data = await request.json()
        fase_id = data.get("fase_id")
        completata = data.get("completata", False)
        utente_id = data.get("utente_id", "anonimo")

        logger.info(f"🔔 Fase completata: {fase_id} | Utente: {utente_id} | Stato: {completata}")

        return {
            "status": "ok",
            "messaggio": f"Fase {fase_id} notificata con successo"
        }

    except Exception as e:
        logger.error(f"❌ Errore nella notifica della fase: {str(e)}")
        raise HTTPException(status_code=500, detail="Errore interno nella notifica fase")

# 🔔 Funzione per inviare notifica automatica al completamento della fase
def notifica_fase_completata(fase_id: str, utente_id: str = "default"):
    url = "https://evoluto.capitaleaziendale.it/notifica_fase"
    payload = {
        "fase_id": fase_id,
        "completata": True,
        "utente_id": utente_id
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"✅ Notifica inviata per la fase {fase_id}")
        return {"status": "ok"}
    except Exception as ex:
        print(f"❌ Errore notifica fase: {str(ex)}")
        return {"status": "errore", "errore": str(ex)}
