from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from modulo_filtra_bandi import filtra_bandi
import pandas as pd
import requests
import os
import logging

# 🔧 Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 🔐 Variabili ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 🧾 Input atteso da GPT
class AziendaInput(BaseModel):
    codice_ateco: str
    regione: str
    dimensione: str
    macroarea: Literal["sostegno", "innovazione"]

# 🔗 Endpoint principale
@app.post("/filtra-bandi")
async def filtra_bandi_per_azienda(input_data: AziendaInput):
    logger.info(f"✅ Ricevuti dati da eVoluto: {input_data.dict()}")

    # ✅ Selezione tabella per macroarea
    if input_data.macroarea == "sostegno":
        tabella = "bandi_sostegno"
    elif input_data.macroarea == "innovazione":
        tabella = "bandi_innovazione"
    else:
        raise HTTPException(status_code=400, detail="Macroarea non valida")

    logger.info(f"✅ Macroarea selezionata: {tabella}")

    # ✅ Recupero dati da Supabase
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    url = f"{SUPABASE_URL}/{tabella}"
    logger.info(f"📡 Chiamata a Supabase: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error(f"❌ Errore Supabase [{response.status_code}]: {response.text}")
        raise HTTPException(status_code=500, detail="Errore nel recupero dati da Supabase")

    dati = response.json()
    logger.info(f"📥 Dati ricevuti: {len(dati)} record")
    df = pd.DataFrame(dati)

    if df.empty:
        return {"bandi": [], "messaggio": "Nessun bando disponibile"}

    # ✅ Filtro bandi
    df_filtrati = filtra_bandi(
        df,
        codice_ateco=input_data.codice_ateco,
        regione=input_data.regione,
        dimensione=input_data.dimensione
    )

    if df_filtrati.empty:
        return {"bandi": [], "messaggio": "Nessun bando compatibile trovato"}

    # ✅ Colonne da restituire
    colonne_da_esporre = [
        "Titolo", "Descrizione", "Obiettivo_Finalita",
        "Data_chiusura", "Forma_agevolazione", "Regioni"
    ]
    colonne_presenti = [col for col in colonne_da_esporre if col in df_filtrati.columns]

    logger.info(f"👉 Colonne presenti: {df_filtrati.columns.tolist()}")
    logger.info(f"👉 Colonne da esporre: {colonne_presenti}")

    colonne_fondamentali = {"Titolo", "Obiettivo_Finalita", "Forma_agevolazione"}
    if not colonne_fondamentali.issubset(df_filtrati.columns):
        raise HTTPException(status_code=500, detail="Dati incompleti nei bandi filtrati")

    # ✅ Output
    bandi_output = df_filtrati[colonne_presenti].head(3).to_dict(orient="records")
    return {"bandi": bandi_output}
