from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
import pandas as pd
import requests
import os
from modulo_filtra_bandi import filtra_bandi

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
        # ✅ Selezione dinamica della tabella
        if input_data.macroarea == "sostegno":
            tabella = "bandi_sostegno"
        elif input_data.macroarea == "innovazione":
            tabella = "bandi_innovazione"
        else:
            raise HTTPException(status_code=400, detail="Macroarea non valida")

        # ✅ Recupero dati da Supabase
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        response = requests.get(f"{SUPABASE_URL}/{tabella}", headers=headers)
        if response.status_code != 200:
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
            "Data_apertura", "Data_chiusura", "Dimensioni",
            "Forma_agevolazione", "Codici_ATECO", "Regioni", "Ambito_territoriale"
        ]
        df_finale = df_filtrati[colonne_da_esporre].head(3)

        return {"bandi": df_finale.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
