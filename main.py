import json
from query_supabase import recupera_bandi_filtrati
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from client_claude import chiama_claude
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

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
    macro_area: Optional[str]

@app.post("/analizza-azienda")
async def analizza_azienda(dati: InputDati):
    logger.info("Dati ricevuti: %s", dati.json())

    try:
        # Validazione input
        if not dati.anagrafica or not dati.bilancio:
            raise HTTPException(status_code=400, detail="Dati incompleti")

        # Placeholder logica Z-Score e MCC stimati
        z_score = stima_z_score(dati.bilancio)
        mcc_rating = stima_mcc(dati.bilancio)

        logger.info("Z-Score stimato: %s", z_score)
        logger.info("MCC rating stimato: %s", mcc_rating)

        # Recupero bandi da Supabase in base a macro-area
        bandi = recupera_bandi_filtrati(
            macro_area=dati.macro_area,
            codice_ateco=dati.anagrafica.codice_ateco,
            regione=dati.anagrafica.regione
        )

        logger.info("Bandi recuperati: %d", len(bandi))

        # Chiamata a Claude per selezione finale
        risposta_claude = chiama_claude(bandi, z_score, mcc_rating, utile_netto)
        logger.info("Risposta Claude ricevuta")

        return {
            "macro_area": dati.macro_area,
            "dimensione": dimensione_azienda(dati.anagrafica),
            "z_score": z_score,
            "mcc_rating": mcc_rating,
            "bandi_filtrati": bandi
        }

    except Exception as e:
        logger.exception("Errore durante l'elaborazione")
        raise HTTPException(status_code=500, detail=str(e))

def stima_z_score(bilancio: Bilancio) -> float:
    # Formula semplificata (proxy)
    if bilancio.totale_attivo and bilancio.utile_netto:
        return round((bilancio.utile_netto / bilancio.totale_attivo) * 3.5, 2)
    return 1.5  # Valore medio stimato

def stima_mcc(bilancio: Bilancio) -> int:
    # MCC stimato da utile e EBITDA
    if bilancio.utile_netto > 0 and bilancio.ebitda > 0:
        return 2
    elif bilancio.utile_netto > 0:
        return 3
    return 4

def recupera_bandi_filtrati(macro_area: str, codice_ateco: Optional[str], regione: Optional[str]):
    # MOCK: sostituire con query a Supabase
    bandi_mock = [
        {"titolo": "Bando Innovazione", "regione": regione, "settore": codice_ateco, "macro_area": macro_area},
        {"titolo": "Bando Digitalizzazione", "regione": regione, "settore": codice_ateco, "macro_area": macro_area}
    ]
    return bandi_mock

def dimensione_azienda(anagrafica: Anagrafica) -> str:
    dipendenti = anagrafica.numero_dipendenti or 0
    if dipendenti <= 10:
        return "Microimpresa"
    elif dipendenti <= 50:
        return "Piccola impresa"
    elif dipendenti <= 250:
        return "Media impresa"
    return "Grande impresa"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
