from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from modulo_filtra_bandi_clean import filtra_bandi
import pandas as pd
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 🔐 Variabili ambiente (Render/Supabase)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 🧾 Input atteso da GPT (dopo lettura bilancio)
class AziendaInput(BaseModel):
    codice_ateco: str
    regione: str
    dimensione: str
    macroarea: Literal["sostegno", "innovazione"]

# 🔗 Endpoint principale
@app.post("/filtra-bandi")
async def filtra_bandi_per_azienda(input_data: AziendaInput):
    logger.info("📡 Entrata nella funzione filtra_bandi_per_azienda")
    logger.info(f"✅ Contenuto input_data ricevuto: {input_data}")

    try:
        logger.info(f"✅ Ricevuti dati da eVoluto: {input_data.dict()}")
        # ✅ Selezione dinamica della tabella
        if input_data.macroarea == "sostegno":
            tabella = "bandi_sostegno"
        elif input_data.macroarea == "innovazione":
            tabella = "bandi_innovazione"
        else:
            raise HTTPException(status_code=400, detail="Macroarea non valida")

        logger.info(f"✅ Macroarea selezionata: {tabella}")
        logger.info(f"📲 Interrogata la Macroarea → {SUPABASE_URL}/{tabella}")

        # ✅ Recupero dati da Supabase
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{tabella}?select=*"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logger.error(f"❌ Errore Supabase [{response.status_code}]: {response.text}")
            raise HTTPException(status_code=500, detail="Errore nel recupero dati da Supabase")

        # 🩹 Fix struttura dati
        dati_json = response.json()
        if isinstance(dati_json, dict):
            dati_json = [dati_json]

        try:
            df = pd.DataFrame(dati_json)
            logger.info(f"✅ DataFrame creato: {df.shape[0]} righe, {df.shape[1]} colonne")
            logger.info(f"🔍 Colonne presenti nel DataFrame: {df.columns.tolist()}")
        except Exception as e:
            logger.error(f"❌ Errore nella creazione del DataFrame: {str(e)}")
            raise HTTPException(status_code=500, detail="Errore nella lettura dei dati dai bandi")

        if df.empty:
            return {"bandi": [], "messaggio": "Nessun bando disponibile"}

        # ✅ Filtro sui dati
        try:
            df_filtrati = filtra_bandi(
                df,
                codice_ateco=input_data.codice_ateco,
                regione=input_data.regione,
                dimensione=input_data.dimensione
            )
            logger.info(f"✅ Filtro bandi completato: {len(df_filtrati)} bandi trovati")
        except Exception as e:
            logger.error(f"❌ Errore nel filtraggio dei bandi: {str(e)}")
            raise HTTPException(status_code=500, detail="Errore nel filtraggio dei bandi")

        if df_filtrati.empty:
            return {"bandi": [], "messaggio": "Nessun bando compatibile trovato"}

        colonne_da_esporre = [
            "Titolo", "Descrizione", "Obiettivo_Finalita",
            "Data_chiusura", "Forma_agevolazione", "Regioni",
        ]

        colonne_presenti = [col for col in colonne_da_esporre if col in df_filtrati.columns]

        logger.info(f"👉 Colonne disponibili in df_filtrati: {df_filtrati.columns.tolist()}")
        logger.info(f"👉 Colonne da esporre: {colonne_da_esporre}")
        logger.info(f"👉 Colonne effettivamente presenti: {colonne_presenti}")

        colonne_fondamentali = {"Titolo", "Obiettivo_Finalita", "Forma_agevolazione"}
        if not colonne_fondamentali.issubset(set(colonne_presenti)):
            logger.error(f"❌ Errore: colonne fondamentali mancanti")
            raise HTTPException(status_code=500, detail="Colonne fondamentali mancanti")

        # ✅ Output finale
        return {
            "bandi": df_filtrati[colonne_presenti].to_dict(orient="records"),
            "totale": len(df_filtrati)
        }

    except Exception as e:
        logger.error(f"❌ Errore generale: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
