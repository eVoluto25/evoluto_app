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
    return response.data

@app.get("/bandi-sostegno")
def get_bandi_sostegno():
    response = supabase.table("bandi_sostegno").select("*").execute()
    return response.data

@app.get("/bandi-innovazione")
def get_bandi_innovazione():
    response = supabase.table("bandi_innovazione").select("*").execute()
    return response.data

@app.get("/bandi-transizione")
def get_bandi_transizione():
    response = supabase.table("bandi_transizione").select("*").execute()
    return response.data
