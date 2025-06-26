import os
import pandas as pd
from fastapi import FastAPI
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

def prepara_output_per_gpt(df_input: pd.DataFrame) -> dict:
    campi_richiesti = [
        "Titolo",
        "Descrizione",
        "Obiettivo_Finalita",
        "Data_apertura",
        "Data_chiusura",
        "Dimensioni",
        "Tipologia_Soggetto",
        "Forma_agevolazione",
        "Codici_ATECO",
        "Regioni",
        "Ambito_territoriale"
    ]
    output = df_input[campi_richiesti].to_dict(orient="records")
    return {"bandi_rilevanti": output}

# Connessione Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/bandi-attivi")
def leggi_bandi_attivi():
    response = supabase.table("bandi_attivi_filtrati").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando attivo disponibile."
        }
    df = pd.DataFrame(response.data)
    return prepara_output_per_gpt(df)


@app.get("/bandi-sostegno")
def get_bandi_sostegno():
    response = supabase.table("bandi_sostegno").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando disponibile nella categoria sostegno."
        }
    df = pd.DataFrame(response.data)
    return prepara_output_per_gpt(df)

@app.get("/bandi-innovazione")
def get_bandi_innovazione():
    response = supabase.table("bandi_innovazione").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando disponibile nella categoria innovazione."
        }
    df = pd.DataFrame(response.data)
    return prepara_output_per_gpt(df)

@app.get("/bandi-transizione")
def get_bandi_transizione():
    response = supabase.table("bandi_transizione").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando disponibile nella categoria transizione."
        }
    df = pd.DataFrame(response.data)
    return prepara_output_per_gpt(df)


@app.get("/bandi-digitalizzazione")
def get_bandi_digitalizzazione():
    response = supabase.table("bandi_digitalizzazione").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando disponibile nella categoria digitalizzazione."
        }
    df = pd.DataFrame(response.data)
    return prepara_output_per_gpt(df)
