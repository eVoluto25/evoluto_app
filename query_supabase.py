from typing import List, Tuple
from supabase import create_client, Client
import os

# Connessione Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def recupera_bandi_completi(macroarea: str, codice_ateco: str, dimensione: str, oggi: str) -> List[dict]:
    tabella = "bandi_sostegno" if macroarea == "Sostegno" else "bandi_innovazione"

    response = supabase.table(tabella) \
        .select("*") \
        .gte("Data_chiusura", oggi) \
        .or_(f"Codici_ATECO.ilike.%{codice_ateco}%,Codici_ATECO.eq.tutti i settori") \
        .or_(f"Dimensioni.ilike.%{dimensione}%,Dimensioni.eq.tutte") \
        .execute()

    bandi = []
    for row in response.data:
        bandi.append({
            "ID_Incentivo": row.get("ID_Incentivo", ""),
            "Titolo": row.get("Titolo", ""),
            "Obiettivo_finalita": row.get("Obiettivo_Finalita", ""),
            "Data_apertura": row.get("Data_apertura", ""),
            "Data_chiusura": row.get("Data_chiusura", ""),
            "Dimensioni": row.get("Dimensioni", ""),
            "Forma_agevolazione": row.get("Forma_agevolazione", ""),
            "Spesa_Ammessa_max": row.get("Spesa_Ammessa_max", 0),
            "Agevolazione_Concedibile_max": row.get("Agevolazione_Concedibile_max", 0),
            "Codici_ATECO": row.get("Codici_ATECO", ""),
            "Regioni": row.get("Regioni", ""),
            "Descrizione": row.get("Descrizione", ""),
            "Note_di_apertura_chiusura": row.get("Note_di_apertura_chiusura", ""),
            "Tipologia_Soggetto": row.get("Tipologia_Soggetto", ""),
            "Stanziamento_incentivo": row.get("Stanziamento_incentivo") or 0,
            "Link_istituzionale": row.get("Link_istituzionale", "")
        })

    return bandi

def somma_agevolazioni_macroarea(macro_area: str) -> Tuple[float, List[dict]]:
    tabella = {
        "Sostegno": "bandi_sostegno",
        "Innovazione": "bandi_innovazione"
    }.get(macro_area)

    if not tabella:
        return round(0 / 1_000_000, 2), []

    response = supabase.table(tabella).select("Agevolazione_Concedibile_max").execute()
    bandi_raw = response.data

    totale = 0.0
    bandi_validi = []

    for bando in bandi_raw:
        try:
            importo = float(bando.get("Agevolazione_Concedibile_max") or 0)
            totale += importo
            bandi_validi.append(bando)
        except Exception:
            continue

    return round(totale / 1_000_000, 2), bandi_validi
