from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_bandi():
    response = supabase.table("bandi").select("titolo,descrizione").execute()
    if response.error:
        raise ValueError("Errore nel recupero bandi da Supabase")

    bandi_testo = "\n\n".join(
        f"TITOLO: {b['titolo']}\nDESCRIZIONE: {b['descrizione']}" for b in response.data
    )
    return bandi_testo
