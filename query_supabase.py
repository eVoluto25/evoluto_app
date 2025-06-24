from typing import Optional, Tuple, List
from supabase import create_client, Client
import os

TABELLE_SUPABASE = {
    "Crisi": "bandi_crisi",
    "Sviluppo": "bandi_crescita",
    "Espansione": "bandi_espansione"
}

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def recupera_bandi_filtrati(macro_area: str, codice_ateco: Optional[str] = None, regione: Optional[str] = None, forma_giuridica: Optional[str] = None):

    print(f">>> Debug: macro_area passata = {macro_area}")  
    tabella = {
        "Crisi": "bandi_crisi",
        "Sviluppo": "bandi_crescita",
        "Espansione": "bandi_espansione"
    }.get(macro_area)

    print(f">>> Debug: macro_area = {macro_area}, tabella = {tabella}")
    print(f">>> Debug: codice_ateco = {codice_ateco}, regione = {regione}, forma_giuridica = {forma_giuridica}")

    if not tabella:
        print(">>> Debug: macro_area non valida, nessuna tabella associata")  
        return []

    query = supabase.table(tabella).select("*")
    if codice_ateco:
        query = query.or_(
            f"Codici_ATECO.ilike.%{codice_ateco}%,Codici_ATECO.ilike.%tutti%"
        )
        print(f">>> Debug: filtro Codici_ATECO = {codice_ateco} (con fallback su 'tutti')")

    if regione:
        query = query.or_(
            f"Regioni.ilike.%{regione}%,Regioni.ilike.%tutte%"
        )
        print(f">>> Debug: filtro Regione = {regione} (con fallback su 'tutte')")
        
    if forma_giuridica and tabella == "bandi_disponibili":
        query = query.eq("Forma_giuridica", forma_giuridica)
        print(f">>> Debug: filtro Forma_giuridica = {forma_giuridica}")
        
    result = query.execute().data
    print(f">>> Debug: risultati trovati = {len(result)}")
    return result
    
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

def recupera_dettagli_bando(ID_Incentivo: str, forma_giuridica_azienda: str) -> dict:
    response = supabase.table("bandi_disponibili").select("*").eq("ID_Incentivo", ID_Incentivo).single().execute()
    row = response.data

    if not row:
        return {}

    # Controllo compatibilità forma giuridica
    forme_ammesse = row.get("Forma_giuridica", "")
    if forme_ammesse:
        forma_giuridica_azienda = forma_giuridica_azienda.lower()
        forme_ammesse_lower = forme_ammesse.lower()
        if forma_giuridica_azienda not in forme_ammesse_lower:
            return {}  # Bando non compatibile

    return {
        "Descrizione": row.get("Descrizione", ""),
        "Note_di_apertura_chiusura": row.get("Note_di_apertura_chiusura", ""),
        "Tipologia_Soggetto": row.get("Tipologia_Soggetto", ""),
        "Stanziamento_incentivo": row.get("Stanziamento_incentivo") or 0,
        "Link_istituzionale": row.get("Link_istituzionale", "")
    }

    return round(totale / 1_000_000, 2), bandi
