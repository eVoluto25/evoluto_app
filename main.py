from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modulo_filtra_bandi import filtra_bandi
from scoring_bandi import calcola_scoring_bandi
import pandas as pd
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 🔗 URL del JSON su GitHub
JSON_URL = "https://raw.githubusercontent.com/eVoluto25/evoluto_app/refs/heads/main/opendata-export.json"

# 🧾 Input atteso da GPT
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

@app.post("/filtra-bandi")
async def filtra_bandi_per_azienda(input_data: AziendaInput):
    logger.info("📡 Entrata nella funzione filtra_bandi_per_azienda")
    logger.info(f"✅ Contenuto input_data ricevuto: {input_data}")
    try:
        logger.info(f"✅ Ricevuti dati da eVoluto: {input_data.dict()}")

        # 🔄 Carica i dati JSON da GitHub
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
            max_results=30
        )

        if not bandi_filtrati:
            return {"bandi": [], "messaggio": "Nessun bando compatibile trovato"}

        # ✅ Calcola scoring finale
        from scoring_bandi import calcola_scoring_bandi

        bandi_finali = calcola_scoring_bandi(
            bandi=bandi_filtrati,
            azienda={
                "regione": input_data.regione,
                "ebitda": 249121,  # oppure input_data.ebitda se lo ricevi
                "utile_netto": 124128,
                "fatturato": 925439
            },
        )

        # ✅ Restituisci lista finale già pronta
        return {
            "bandi": bandi_filtrati,
            "totale": len(bandi_filtrati)
        }

    except Exception as e:
        logger.error(f"❌ Errore generale: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
