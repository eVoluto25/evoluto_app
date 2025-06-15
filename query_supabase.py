from supabase import create_client
import os

# Collegamento a Supabase tramite chiavi salvate su Render
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def recupera_bandi_filtrati((macro_area, codice_ateco, regione):
    tabella_mapping = {
        "Crisi o Risanamento Aziendale": "bandi_crisi",
        "Crescita e Sviluppo": "bandi_crescita",
        "Espansione e Transizione": "bandi_espansione"
    }

    nome_tabella = tabella_mapping.get(macro_area)
    if not nome_tabella:
        return []

    try:
        response = supabase.table(nome_tabella).select("*").execute()
        bandi = response.data
    except Exception as e:
        print(f"Errore nella query Supabase: {e}")
        return []

    bandi_filtrati = []
    for bando in bandi:
        codici_ateco_bando = bando.get("Codici_ATECO", "").lower()
        regione_bando = bando.get("Regione", "").lower()

        ateco_match = (
            "tutti i settori" in codici_ateco_bando or
            codice_ateco.lower() in codici_ateco_bando
        )
        regione_match = (
            regione_bando in ["", "tutte", "tutta italia"] or
            regione.lower() == regione_bando
        )

        if ateco_match and regione_match:
            bandi_filtrati.append(bando)

    return bandi_filtrati
