from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from modulo_filtra_bandi import filtra_bandi
import pandas as pd
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 🔗 URL del JSON su GitHub
JSON_URL = "https://raw.githubusercontent.com/eVoluto25/evoluto_app/refs/heads/main/opendata-export.json"

# 🧾 Input atteso da GPT (dopo lettura bilancio)
class AziendaInput(BaseModel):
    codice_ateco: str
    regione: str
    dimensione: str
    macroarea: Literal["sostegno", "innovazione"]
    forma_agevolazione: str | None = None  # opzionale


# ✅ Funzione di normalizzazione
def normalizza_codici_ateco(x):
    """
    Rende uniforme il campo Codici_ATECO in lista di stringhe.
    """
    if isinstance(x, list):
        return [i.strip() for i in x if i]
    if x is None:
        return []
    if isinstance(x, str):
        return [x.strip()]
    return []

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

        # ✅ Normalizza i codici ATECO
        df["Codici_ATECO"] = df["Codici_ATECO"].apply(normalizza_codici_ateco)

        # 🔍 Log di debug per vedere i dati veri
        logger.info("*** Contenuto normalizzato Codici_ATECO:")
        for idx, riga in enumerate(df["Codici_ATECO"].tolist()):
            logger.info(f"Riga {idx}: {riga}")

        # ✅ Filtra i bandi
        df_filtrati = filtra_bandi(
            df,
            codice_ateco=input_data.codice_ateco,
            regione=input_data.regione,
            dimensione=input_data.dimensione,
            macroarea=input_data.macroarea,
            max_results=5
        )
        logger.info(f"✅ Filtro bandi completato: {len(df_filtrati)} bandi trovati")

        if df_filtrati.empty:
            return {"bandi": [], "messaggio": "Nessun bando compatibile trovato"}

        # ✅ Colonne da esporre (originali dal JSON)
        colonne_da_esporre = [
            "Titolo",
            "Descrizione",
            "Obiettivo_Finalita",
            "Data_chiusura",
            "Dimensioni",
            "Forma_agevolazione",
            "Codici_ATECO",
            "Regioni"
        ]

        colonne_presenti = [col for col in colonne_da_esporre if col in df_filtrati.columns]
        logger.info(f"👉 Colonne disponibili in df_filtrati: {df_filtrati.columns.tolist()}")
        logger.info(f"👉 Colonne effettivamente presenti: {colonne_presenti}")

        colonne_fondamentali = {"Titolo", "Obiettivo_Finalita", "Forma_agevolazione"}
        if not colonne_fondamentali.issubset(set(colonne_presenti)):
            logger.error(f"❌ Colonne fondamentali mancanti: {colonne_fondamentali - set(colonne_presenti)}")
            raise HTTPException(status_code=500, detail="Colonne fondamentali mancanti")

        logger.info(f"✅ Pronto a restituire i risultati")

        return {
            "bandi": df_filtrati[colonne_presenti].to_dict(orient="records"),
            "totale": len(df_filtrati)
        }

    except Exception as e:
        logger.error(f"❌ Errore generale: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
