from supabase import create_client, Client
from typing import List, Dict
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def estrai_bandi(macro_area: str, codice_ateco: str, regione: str, dimensione: str, limite: int = 15) -> List[Dict]:
    tabella_map = {
        "Crisi": "bandi_crisi",
        "Sviluppo": "bandi_crescita",
        "Espansione": "bandi_espansione"
    }

    tabella = tabella_map.get(macro_area)
    if not tabella:
        return []

    query = supabase.table(tabella).select("*")

    # Filtro per regione (se presente o "tutti")
    query = query.or_(f"Regioni.ilike.%{regione}%,Regioni.ilike.%tutti%")

    # Filtro per dimensione (es. "Microimpresa")
    query = query.or_(f"Dimensioni.ilike.%{dimensione}%,Dimensioni.ilike.%tutte%")

    # Filtro per codice ATECO: match puntuale o "tutti i settori"
    query = query.or_(f"Codici_ATECO.ilike.%{codice_ateco}%,Codici_ATECO.ilike.%tutti%")

    response = query.limit(limite).execute()

    return response.data if response.data else []
