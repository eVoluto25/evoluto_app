import os
from fastapi import FastAPI
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

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
    return {"data": response.data, "esito": "ok"}


@app.get("/bandi-sostegno")
def get_bandi_sostegno():
    response = supabase.table("bandi_sostegno").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando disponibile nella categoria sostegno."
        }
    return {"data": response.data, "esito": "ok"}


@app.get("/bandi-innovazione")
def get_bandi_innovazione():
    response = supabase.table("bandi_innovazione").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando disponibile nella categoria innovazione."
        }
    return {"data": response.data, "esito": "ok"}


@app.get("/bandi-transizione")
def get_bandi_transizione():
    response = supabase.table("bandi_transizione").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando disponibile nella categoria transizione."
        }
    return {"data": response.data, "esito": "ok"}


@app.get("/bandi-digitalizzazione")
def get_bandi_digitalizzazione():
    response = supabase.table("bandi_digitalizzazione").select("*").execute()
    if not response.data:
        return {
            "data": [],
            "esito": "nessun_bando",
            "messaggio": "Nessun bando disponibile nella categoria digitalizzazione."
        }
    return {"data": response.data, "esito": "ok"}
