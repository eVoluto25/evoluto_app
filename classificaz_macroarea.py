import uuid
from datetime import datetime
from supabase import create_client, Client
import os

# Connessione Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Variabili d'ambiente SUPABASE_URL o SUPABASE_KEY mancanti.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def popola_verifica_aziendale(dati_bilancio: dict):
    """
    Classifica l'azienda in una macroarea strategica in base agli indici finanziari
    e popola la tabella 'verifica_aziendale' su Supabase.
    """
    # Estrazione degli indici principali
    current_ratio = dati_bilancio.get("current_ratio")
    debt_equity = dati_bilancio.get("debt_equity")
    interest_coverage = dati_bilancio.get("interest_coverage")
    ebitda_margin = dati_bilancio.get("ebitda_margin")
    utile_netto = dati_bilancio.get("utile_netto")

    autofinanziamento = dati_bilancio.get("autofinanziamento")
    solidita = dati_bilancio.get("solidita")
    incidenza_investimenti = dati_bilancio.get("incidenza_investimenti")
    ha_r_and_d = dati_bilancio.get("ha_r_and_d", False)

    crescita_fatturato = dati_bilancio.get("crescita_fatturato")
    ros = dati_bilancio.get("ros")
    investimenti_immobilizzazioni = dati_bilancio.get("investimenti_immobilizzazioni")

    # Logica di classificazione
    area_crisi = (
        (current_ratio is not None and current_ratio < 1) or
        (debt_equity is not None and debt_equity > 2) or
        (interest_coverage is not None and interest_coverage < 1) or
        (ebitda_margin is not None and ebitda_margin < 0.05) or
        (utile_netto is not None and utile_netto < 0)
    )

    area_crescita = (
        (autofinanziamento is not None and autofinanziamento > 0) or
        (solidita is not None and solidita > 0.25) or
        (incidenza_investimenti is not None and incidenza_investimenti > 0.1) or
        ha_r_and_d
    )

    area_espansione = (
        (crescita_fatturato is not None and crescita_fatturato > 0.05) or
        (ros is not None and ros > 0.08) or
        (investimenti_immobilizzazioni is not None and investimenti_immobilizzazioni > 0)
    )

    # Inserimento con flag esclusivi (priorità: Crisi > Crescita > Espansione)
    row = {
        "uuid": str(uuid.uuid4()),
        "inserimento": datetime.now().isoformat(),
        "area_crisi_risanamento": "1" if area_crisi else "0",
        "area_crescita_sviluppo": "1" if not area_crisi and area_crescita else "0",
        "area_espansione_transizione": "1" if not area_crisi and not area_crescita and area_espansione else "0"
    }

    supabase.table("verifica_aziendale").insert(row).execute()
    return row
