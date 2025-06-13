# supabase_client.py

import os
import logging
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("SUPABASE_URL o SUPABASE_KEY non definite")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def inserisci_diagnosi(tabella: str, record: dict):
    try:
        response = supabase.table(tabella).insert(record).execute()
        return response.data
    except Exception as e:
        logging.error(f"Errore inserimento Supabase: {e}")
        return {"errore": str(e)}

def aggiorna_diagnosi(tabella: str, chiave: str, valore: str, aggiornamento: dict):
    try:
        response = supabase.table(tabella).update(aggiornamento).eq(chiave, valore).execute()
        return response.data
    except Exception as e:
        logging.error(f"Errore aggiornamento Supabase: {e}")
        return {"errore": str(e)}

def recupera_bando(tabella: str, id_incentivo: str):
    try:
        response = supabase.table(tabella).select("*").eq("ID_Incentivo", id_incentivo).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        logging.error(f"Errore recupero Supabase: {e}")
        return {"errore": str(e)}