
from supabase import create_client, Client
import os

# Queste chiavi vanno definite come variabili d'ambiente o sostituite direttamente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def fetch_bandi():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table("bandi_disponibili").select("*").execute()
    return response.data if response.data else []
