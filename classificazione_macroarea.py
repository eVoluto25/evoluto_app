import logging
from utils import supabase_insert

logging.basicConfig(level=logging.INFO)

def assegna_macroarea_e_inserisci(indici: dict, anagrafica: dict):
    """
    Assegna la macroarea in base agli indici finanziari e inserisce tutto su Supabase
    """
    macroarea_flags = {
        'area_crisi_risanamento': False,
        'area_crescita_sviluppo': False,
        'area_espansione_transizione': False
    }

    # 🔴 Crisi o Risanamento
    if (
        indici.get("current_ratio", 99) < 1 or
        indici.get("debt_equity", 0) > 2 or
        indici.get("interest_coverage_ratio", 99) < 1 or
        indici.get("ebitda_margin", 99) < 5 or
        indici.get("utile_netto", 0) < 0
    ):
        macroarea_flags['area_crisi_risanamento'] = True

    # 🟠 Crescita e Sviluppo
    elif (
        indici.get("autofinanziamento", 0) > 0 and
        indici.get("patrimonio_netto", 0) / indici.get("totale_attivo", 1) > 0.2 and
        indici.get("immobilizzazioni", 0) / indici.get("totale_attivo", 1) > 0.15
    ):
        macroarea_flags['area_crescita_sviluppo'] = True

    # 🟢 Espansione e Transizione
    else:
        macroarea_flags['area_espansione_transizione'] = True

    logging.info(f"Macroarea assegnata: {macroarea_flags}")

    # 🧩 Composizione finale del record per Supabase
    record = {
        **anagrafica,
        **indici,
        **macroarea_flags,
        'id_incentivo': []  # inizialmente vuoto, sarà popolato da bandi_matcher
    }

    logging.info(f"Inserimento in verifica_aziendale: {record}")
    supabase_insert("verifica_aziendale", record)
    logging.info("Inserimento completato.")
