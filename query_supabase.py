from classifica_bandi import classifica_bandi_avanzata as classifica_bandi
from supabase import create_client
from typing import Optional
import os

# Collegamento a Supabase tramite chiavi salvate su Render
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def recupera_bandi_filtrati(macro_area: str, codice_ateco: Optional[str], regione: Optional[str]):
    tabella = None
    if macro_area == "Crisi":
        tabella = "bandi_crisi"
    elif macro_area == "Sviluppo":
        tabella = "bandi_crescita"
    elif macro_area == "Espansione":
        tabella = "bandi_espansione"
    else:
        return []

    response = supabase.table(tabella).select("*").execute()
    bandi = []

def somma_agevolazioni_macroarea(macro_area: str) -> tuple[float, list]:
    tabella = {
        "Crisi": "bandi_crisi",
        "Sviluppo": "bandi_crescita",
        "Espansione": "bandi_espansione"
    }.get(macro_area)

    if not tabella:
        return 0.0

    response = supabase.table(tabella).select("*").execute()

    agevolazioni = [
        b.get("Agevolazione_Concedibile_max", 0) or 0
        for b in response.data
        if isinstance(b.get("Agevolazione_Concedibile_max", 0), (int, float))
    ]
    totale = sum(agevolazioni)
   
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
