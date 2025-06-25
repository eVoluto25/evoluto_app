from supabase import create_client, Client
import os
import json

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def carica_dati_azienda(contenuto_email: str) -> dict:
    try:
        return json.loads(contenuto_email)
    except Exception as e:
        print(f"Errore nel parsing JSON: {e}")
        return {}

def punteggio_da_risposte(risposte_lettere: List[str]) -> int:
    """
    Converte una lista di risposte multiple (A–E) in un punteggio complessivo.
    A = 5, B = 4, C = 3, D = 2, E = 1. Qualsiasi altro valore = 0.
    """
    mapping = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}
    return sum(mapping.get(r.upper(), 0) for r in risposte_lettere)

def salva_top5_bandi(dati_azienda: dict, top3_bandi: list) -> None:
    dati_azienda["top3_bandi"] = top3_bandi

def supabase_insert(tabella, dati):
    return supabase.table(tabella).insert(dati).execute()

def supabase_query(tabella, macroarea):
    return supabase.table(tabella).select("*").eq("macroarea", macroarea).execute().data

def supabase_query_esteso(tabella, filtro):
    query = supabase.table(tabella).select("*")

    # Macroarea (obbligatoria)
    query = query.eq("macroarea", filtro["macroarea"])

    # Match diretti
    for campo in ["Tipologia_Soggetto", "Dimensioni", "Settore_Attivita"]:
        if filtro[campo]:
            query = query.ilike(campo, f"%{filtro[campo]}%")

    # Codici ATECO (match se incluso nella stringa)
    if filtro["Codici_ATECO"]:
        query = query.ilike("Codici_ATECO", f"%{filtro['Codici_ATECO']}%")

    # Regioni e Comuni (solo se presenti nei dati)
    if filtro.get("Regioni"):
        query = query.or_(f"Regioni.ilike.%{filtro['Regioni']}%,Regioni.is.null")

    if filtro.get("Comuni"):
        query = query.or_(f"Comuni.ilike.%{filtro['Comuni']}%,Comuni.is.null")

    return query.execute().data
