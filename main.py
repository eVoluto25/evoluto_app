from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modulo_filtra_bandi import filtra_bandi
from scoring_bandi import calcola_scoring_bandi
import pandas as pd
import requests
import logging
from typing import List, Dict
from calendar_api import router as calendar_router
from prompt_evoluto import master_flow

import os
from datetime import date
from supabase import create_client

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
            max_results=10
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
    return {"fase": master_flow[fase_id]}
