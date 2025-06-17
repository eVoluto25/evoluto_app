import json
from query_supabase import recupera_bandi_filtrati
from classifica_bandi import classifica_bandi_avanzata as classifica_bandi
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from validazione_online import valida_bando_online_mock
from validazione_google import cerca_google_bando 
from analisi_predittiva_gpt import analizza_benefici_bandi
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def root():
    return "eVoluto è attivo."

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://evoluto.capitaleaziendale.it"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelli input
class Anagrafica(BaseModel):
    codice_ateco: Optional[str] = None
    regione: Optional[str] = None
    forma_giuridica: Optional[str] = None
    numero_dipendenti: Optional[int] = None
    attivita_prevalente: Optional[str] = None

class Bilancio(BaseModel):
    ricavi: Optional[float] = 0
    utile_netto: Optional[float] = 0
    ebitda: Optional[float] = 0
    totale_attivo: Optional[float] = 0
    immobilizzazioni: Optional[float] = 0
    ricavi_anno_prec: Optional[float] = None

class InputDati(BaseModel):
    anagrafica: Anagrafica
    bilancio: Bilancio

# Indicatori economico-finanziari
def stima_z_score(bilancio: Bilancio):
    if not bilancio.totale_attivo or bilancio.totale_attivo == 0:
        return 0
    return round((bilancio.ebitda + bilancio.utile_netto) / bilancio.totale_attivo, 2)

def stima_mcc(bilancio: Bilancio):
    if not bilancio.ricavi or bilancio.ricavi == 0:
        return 0
    return round((bilancio.utile_netto / bilancio.ricavi) * 100, 2)

def assegna_macro_area(bilancio: Bilancio):
    if bilancio.ebitda > 0:
        return "Espansione"
    elif bilancio.ricavi > 0:
        return "Sviluppo"
    return "Crisi"

def dimensione_azienda(anagrafica: Anagrafica) -> str:
    if anagrafica.numero_dipendenti is None:
        return "Non classificabile"
    if anagrafica.numero_dipendenti <= 9:
        return "Microimpresa"
    elif anagrafica.numero_dipendenti <= 49:
        return "Piccola Impresa"
    elif anagrafica.numero_dipendenti <= 249:
        return "Media Impresa"
    return "Grande impresa"

@app.post("/analizza-azienda")
async def analizza_azienda(dati: InputDati):
    logger.info("Dati ricevuti: %s", dati.json())

    try:
        if not dati.anagrafica or not dati.bilancio:
            raise HTTPException(status_code=400, detail="Dati incompleti")

        z_score = stima_z_score(dati.bilancio)
        mcc_rating = stima_mcc(dati.bilancio)
        macro_area = assegna_macro_area(dati.bilancio)
        dimensione = dimensione_azienda(dati.anagrafica)

        bandi = recupera_bandi_filtrati(
            macro_area=macro_area,
            codice_ateco=dati.anagrafica.codice_ateco,
            regione=dati.anagrafica.regione
        )

        azienda = {
            "codice_ateco": dati.anagrafica.codice_ateco,
            "regione": dati.anagrafica.regione,
            "dimensione": dimensione,
            "ebitda": dati.bilancio.ebitda,
            "immobilizzazioni": dati.bilancio.immobilizzazioni,
            "macro_area": macro_area
        }

        top3 = classifica_bandi(bandi, azienda)

        stato_bandi = []
        for bando in top3:
            try:
                validazione = cerca_google_bando(bando.get("titolo"), dati.anagrafica.regione)
            except Exception as e:
                validazione = {
                    "validato": False,
                    "fondi_disponibili": False,
                    "messaggio": f"⚠️ Errore nella validazione Google: {str(e)}"
                }

            stato_bandi.append({
                "titolo": bando.get("titolo"),
                "validato": validazione["validato"],
                "fondi_disponibili": validazione["fondi_disponibili"],
                "esito": validazione["messaggio"]
            })

        output_predittivo = analizza_benefici_bandi(top3, azienda)

        # 🔁 Costruisci lista strutturata per analisi_gpt
        analisi_gpt = []
        for bando, testo in zip(top3, output_predittivo):
            analisi_gpt.append({
                "titolo": bando.get("Titolo", ""),
                "analisi": testo
            })

        # ✅ Costruzione dell’output testuale
        output_finale = genera_output_finale(
            top3, macro_area, dimensione, mcc_rating, z_score,
            analisi_gpt=analisi_gpt,
            validazione_online=stato_bandi
        )
        print("\n\n🪵 LOG COMPLETO OUTPUT:\n")
        print(output_finale)
        print("\n📏 Lunghezza caratteri:", len(output_finale))
        
        return {
            "macro_area": macro_area,
            "dimensione": dimensione,
            "z_score": z_score,
            "mcc_rating": mcc_rating,
            "stato_bandi": stato_bandi,
            "bandi_filtrati": top3,
            "analisi_predittiva": output_predittivo,
            "output_finale": output_finale 
        }

    except Exception as e:
        logger.exception("Errore durante l'elaborazione")
        raise HTTPException(status_code=500, detail=str(e))

# OUTPUT TESTUALE GPT
def genera_output_finale(
    bandi,
    macro_area,
    dimensione,
    mcc_rating,
    z_score,
    analisi_gpt=None,
    validazione_online=None
):
    output = "📌 **Analisi Aziendale**\n"
    output += f"- Macro Area: **{macro_area}**\n"
    output += f"- Dimensione: **{dimensione}**\n"
    output += f"- MCC Rating: **{mcc_rating}**\n"
    output += f"- Z-Score: **{z_score:.2f}**\n"

    output += "\n\n📑 **Top 3 Bandi Selezionati**\n"
    for i, bando in enumerate(bandi, 1):
        output += f"\n**{i}. {bando.get('Titolo', '--')}**\n"
        output += f"- 🎯 Obiettivo: {bando.get('Obiettivo_finalita', '--')}\n"
        output += f"- 💶 Spesa ammessa max: {bando.get('Spesa_Ammessa_max', '--')} €\n"
        output += f"- 🧮 Agevolazione concedibile: {bando.get('Agevolazione_Concedibile_max', '--')} €\n"
        output += f"- 🧾 Forma agevolazione: {bando.get('Forma_agevolazione', '--')}\n"
        output += f"- ⏳ Scadenza: {bando.get('Data_chiusura', '--')}\n"

        # 🔍 Verifica online integrata e Analisi predittiva integrata
        if validazione_online:
            match = next((v for v in validazione_online if v.get("titolo") == bando.get("Titolo")), None)
            if match:
                output += f"- 🔍 Verifica online: {match.get('messaggio', 'N/D')}\n"
             
    return output
