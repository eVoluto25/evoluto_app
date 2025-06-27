import logging
from typing import List
from supabase import create_client, Client
from pathlib import Path

logger = logging.getLogger(__name__)

SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your-anon-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def filtra_bandi(
    df: pd.DataFrame,
    regione: str,
    codice_ateco: str,
    dimensione: str,
    forma_agevolazione: str,
    max_results: int = 5
) -> pd.DataFrame:
    logger.info(">>> Filtro regione: %s", regione)
    logger.info(">>> Filtro codice ATECO: %s", codice_ateco)
    logger.info(">>> Filtro dimensione: %s", dimensione)
    logger.info(">>> Filtro forma agevolazione: %s", forma_agevolazione)
    logger.info(">>> Filtro obiettivo: %s", obiettivo)

    query = (
    supabase.table("bandi_disponibili")
    .select("*")
    .filter("regioni_clean", "cs", regione)
    .filter("codici_ateco_clean", "cs", codice_ateco)
    .filter("dimensioni_clean", "cs", dimensione)
    .filter("forma_agevolazione_clean", "cs", forma_agevolazione)
    .filter("obiettivo_clean", "eq", obiettivo)
)

    response = query.execute()
    data = response.data or []
    logger.info(f">>> Bandi trovati: {len(data)}")
    return data
