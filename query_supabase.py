from typing import Optional, Tuple, List
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def recupera_bandi_filtrati(macro_area: str, codice_ateco: Optional[str] = None, regione: Optional[str] = None):
    tabella = {
        "Crisi": "bandi_crisi",
        "Sviluppo": "bandi_crescita",
        "Espansione": "bandi_espansione"
    }.get(macro_area)

    if not tabella:
        return []

    response = supabase.table(tabella).select("*").execute()

    bandi = []
    for row in response.data:
        bandi.append({
            "ID_Incentivo": row["ID_Incentivo"],
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

    return bandi


def somma_agevolazioni_macroarea(macro_area: str) -> Tuple[float, List[dict]]:
    tabella = {
        "Crisi": "bandi_crisi",
        "Sviluppo": "bandi_crescita",
        "Espansione": "bandi_espansione"
    }.get(macro_area)

    if not tabella:
        return round(0 / 1_000_000, 2), []

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
            "ID_Incentivo": row["ID_Incentivo"],
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

def recupera_dettagli_bando(ID_Incentivo: str) -> dict:
    response = supabase.table("bandi_disponibili").select("*").eq("ID_Incentivo", ID_Incentivo).single().execute()
    row = response.data
    return {
        "Descrizione": row.get("Descrizione", ""),
        "Note_di_apertura_chiusura": row.get("Note_di_apertura_chiusura", ""),
        "Tipologia_Soggetto": row.get("Tipologia_Soggetto", ""),
        "Stanziamento_incentivo": row.get("Stanziamento_incentivo") or 0,
        "Link_istituzionale": row.get("Link_istituzionale", "")
    } if row else {}

    return round(totale / 1_000_000, 2), bandi
