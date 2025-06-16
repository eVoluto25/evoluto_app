import json
from query_supabase import recupera_bandi_filtrati
from classifica_bandi import classifica_bandi 
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
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

@app.post("/analizza-azienda")
async def analizza_azienda(dati: InputDati):
    logger.info("Dati ricevuti: %s", dati.json())

    try:
        if not dati.anagrafica or not dati.bilancio:
            raise HTTPException(status_code=400, detail="Dati incompleti")

        # Calcolo indicatori economici
        z_score = stima_z_score(dati.bilancio)
        mcc_rating = stima_mcc(dati.bilancio)
        macro_area = assegna_macro_area(dati.bilancio)
        dimensione = dimensione_azienda(dati.anagrafica)

        logger.info("Z-Score stimato: %s", z_score)
        logger.info("MCC rating stimato: %s", mcc_rating)

        # Recupero bandi
        bandi = recupera_bandi_filtrati(
            macro_area=macro_area,
            codice_ateco=dati.anagrafica.codice_ateco,
            regione=dati.anagrafica.regione
        )

        logger.info("Bandi recuperati: %d", len(bandi))

        # Costruzione profilo aziendale
        azienda = {
            "codice_ateco": dati.anagrafica.codice_ateco,
            "regione": dati.anagrafica.regione,
            "dimensione": dimensione,
            "ebitda": dati.bilancio.ebitda,
            "immobilizzazioni": dati.bilancio.immobilizzazioni,
            "macro_area": macro_area
        }

        # Classifica e seleziona i migliori 3 bandi
        top3 = classifica_bandi(bandi, azienda)

        return {
            "macro_area": macro_area,
            "dimensione": dimensione,
            "z_score": z_score,
            "mcc_rating": mcc_rating,
            "bandi_filtrati": top3
            "output_predittivo": analizza_benefici_bandi(top3, azienda)
            "output_testuale": output_finale
            "analisi_predittiva": output_predittivo  # 🧠 Risultato GPT
        }

    except Exception as e:
        logger.exception("Errore durante l'elaborazione")
        raise HTTPException(status_code=500, detail=str(e))

# Funzioni di supporto
def stima_z_score(bilancio: Bilancio) -> float:
    if bilancio.totale_attivo and bilancio.utile_netto:
        return round((bilancio.utile_netto / bilancio.totale_attivo) * 3.5, 2)
    return 1.5

def stima_mcc(bilancio: Bilancio) -> int:
    if bilancio.utile_netto > 0 and bilancio.ebitda > 0:
        return 2
    elif bilancio.utile_netto > 0:
        return 3
    return 4

def assegna_macro_area(bilancio: Bilancio) -> str:
    ricavi = bilancio.ricavi or 0
    ebitda = bilancio.ebitda or 0
    immobilizzazioni = bilancio.immobilizzazioni or 0

    if ricavi < 150000 or ebitda < 10000:
        return "Crisi"
    if ricavi < 1000000 and immobilizzazioni < 200000:
        return "Sviluppo"
    if ricavi >= 1000000 and immobilizzazioni >= 200000:
        return "Espansione"
    return "Sviluppo"

def dimensione_azienda(anagrafica: Anagrafica) -> str:
    dipendenti = anagrafica.numero_dipendenti or 0
    if dipendenti <= 10:
        return "Microimpresa"
    elif dipendenti <= 50:
        return "Piccola impresa"
    elif dipendenti <= 250:
        return "Media impresa"
    return "Grande impresa"

def genera_output_finale(bandi, macro_area, dimensione, mcc, z_score):
    output = f"""
📂 Macro Area Assegnata: {macro_area}
📊 Dimensione Impresa: {dimensione}
🔐 MCC Rating: {mcc}
📉 Z-Score stimato: {z_score}

📌 eVoluto ha analizzato +300 bandi pubblici. Ecco i 3 più coerenti con la tua struttura aziendale:
"""
    for i, bando in enumerate(bandi, 1):
        output += f"""
{i}. 🏆 **{bando.get('titolo', 'Senza titolo')}**
   - 🎯 Obiettivo: {bando.get('Obiettivo_Finalita', '-')}
   - 💬 Motivazione: {bando.get('Motivazione', '-')}
   - 💰 Spesa ammessa max: {bando.get('Spesa_Ammessa_max', '-')}
   - 💸 Agevolazione concedibile: {bando.get('Agevolazione_Concedibile_max', '-')}
   - 🧾 Forma agevolazione: {bando.get('Forma_agevolazione', '-')}
   - ⏳ Scadenza: {bando.get('Data_chiusura', '-')}
"""

    output += "\n📍 Puoi usare queste informazioni per valutare la candidatura ai bandi più adatti."
    return output

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
