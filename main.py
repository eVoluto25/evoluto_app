from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import requests
import os
from modulo_filtra_bandi import filtra_bandi

app = FastAPI()

# 🔐 Variabili ambiente (Render/Supabase)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 🧾 Modello dati ricevuti da GPT
class AziendaInput(BaseModel):
    codice_ateco: str
    regione: str
    dimensione: str
    forma_agevolazione: Optional[str] = None

# 🔗 Endpoint principale
@app.post("/filtra-bandi")
async def filtra_bandi_per_azienda(input_data: AziendaInput):
    try:
        # ✅ Recupero tabella bandi da Supabase
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }

        response = requests.get(f"{SUPABASE_URL}/bandi_view", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Errore nel recupero dati da Supabase")

        df = pd.DataFrame(response.json())
        if df.empty:
            raise HTTPException(status_code=404, detail="Nessun bando disponibile")

        # ✅ Applico il filtro
        df_filtrati = filtra_bandi(
            df,
            codice_ateco=input_data.codice_ateco,
            regione=input_data.regione,
            dimensione=input_data.dimensione,
            forma_agevolazione=input_data.forma_agevolazione
        )

        if df_filtrati.empty:
            return {"bandi": [], "messaggio": "Nessun bando compatibile trovato"}

        # ✅ Seleziono solo le colonne rilevanti
        colonne_da_esporre = [
            "Titolo", "Descrizione", "Obiettivo_Finalita",
            "Data_apertura", "Data_chiusura", "Dimensioni",
            "Forma_agevolazione", "Codici_ATECO", "Regioni", "Ambito_territoriale"
        ]
        df_finale = df_filtrati[colonne_da_esporre].head(3)
        return {"bandi": df_finale.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Endpoint di test base
@app.get("/")
def root():
    return {"status": "eVoluto API attiva"}
