from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from modulo_filtra_bandi import filtra_bandi
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
    try:
        logger.info(f"✅ Ricevuti dati da GPT: {input_data.dict()}")
        # ✅ Selezione dinamica della tabella
        if input_data.macroarea == "sostegno":
            tabella = "bandi_sostegno"
        elif input_data.macroarea == "innovazione":
            tabella = "bandi_innovazione"
        else:
            raise HTTPException(status_code=400, detail="Macroarea non valida")

        logger.info(f"📦 Tabella selezionata: {tabella}")

        logger.info(f"🌐 Chiamata a Supabase → {SUPABASE_URL}/{tabella}")

        # ✅ Recupero dati da Supabase
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        response = requests.get(f"{SUPABASE_URL}/{tabella}", headers=headers)
        if response.status_code != 200:
            logger.info(f"✅ Risposta Supabase OK - {len(response.json())} bandi trovati")
        else:
            logger.error(f"❌ Errore Supabase [{response.status_code}]: {response.text}")
            raise HTTPException(status_code=500, detail="Errore nel recupero dati da Supabase")

        df = pd.DataFrame(response.json())
        if df.empty:
            return {"bandi": [], "messaggio": "Nessun bando disponibile"}

        # ✅ Filtro sui dati
        df_filtrati = filtra_bandi(
            df,
            codice_ateco=input_data.codice_ateco,
            regione=input_data.regione,
            dimensione=input_data.dimensione
        )

        if df_filtrati.empty:
            return {"bandi": [], "messaggio": "Nessun bando compatibile trovato"}

        # ✅ Output mirato
        colonne_da_esporre = [
            "Titolo", "Descrizione", "Obiettivo_Finalita",
            "Data_chiusura", "Forma_agevolazione", "Regioni",  
        ]
        colonne_presenti = [col for col in colonne_da_esporre if col in df_filtrati.columns]
        colonne_mancanti = set(colonne_da_esporre) - set(df_filtrati.columns)
        logger.warning(f"⚠️ Colonne mancanti nel risultato Supabase: {colonne_mancanti}")

        # 🔒 Protezione da crash se nessuna colonna è presente
        if not colonne_presenti:
            return {"bandi": [], "messaggio": "Errore: nessuna colonna disponibile nei risultati Supabase"}

        df_finale = df_filtrati[colonne_presenti].head(3)

        return {"bandi": df_finale.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
