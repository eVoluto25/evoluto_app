from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

# Connessione Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/bandi-attivi")
def leggi_bandi_attivi():
    response = supabase.table("bandi_attivi_filtrati").select("*").execute()
    return response.data
