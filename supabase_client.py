# supabase_client.py

from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def inserisci_diagnosi(tabella: str, record: dict):
    try:
        supabase.table(tabella).insert(record).execute()
        return True
    except Exception as e:
        return {"error": f"Errore Supabase: {str(e)}"}
