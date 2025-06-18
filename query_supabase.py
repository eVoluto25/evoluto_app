from typing import Optional, Tuple, List
from supabase import create_client
import os

# Connessione al client Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def somma_agevolazioni_macroarea(macro_area: str) -> Tuple[float, List[dict]]:
    tabella = {
        "Crisi": "bandi_crisi",
        "Sviluppo": "bandi_crescita",
        "Espansione": "bandi_espansione"
    }.get(macro_area)

    if not tabella:
        return 0.0, []

    response = supabase.table(tabella).select("*").execute()

    totale = 0
    for bando in response.data:
        val = bando.get("Agevolazione_Concedibile_max", "0")
        if isinstance(val, str):
            val = val.replace("€", "").replace(".", "").replace(",", ".").strip()
        try:
            totale += float(val)
        except (ValueError, TypeError):
            continue

    bandi = []
    for row in response.data:
        bandi.append({
            "ID_incentivo": row["ID_Incentivo"],
            "Titolo": row["Titolo"],
            "Obiettivo_finalita": row["Obiettivo_Finalita"],
            "Data_apertura": row["Data_apertura"],
            "Data_chiusura": row["Data_chiusura"],
            "Dimensioni": row["Dimensioni"],
            "Forma_agevolazione": row["Forma_agevolazione"],
            "Spesa_Ammessa_max": row["Spesa_Ammessa_max"],
            "Agevolazione_Concedibile_max": row["Agevolazione_Concedibile_max"],
            "Codici_ATECO": row["Codici_ATECO"],
            "Regioni": row["Regioni"]
        })

    return round(totale / 1_000_000, 2), bandi  # Totale in milioni + bandi
