import re
import logging

def estrai_dati_identificativi(dati_visura: dict) -> dict:
    return {
        "codice_ateco": dati_visura.get("codice_ateco"),
        "forma_giuridica": dati_visura.get("forma_giuridica"),
        "partita_iva": dati_visura.get("partita_iva"),
        "attivita_prevalente": dati_visura.get("attivita_prevalente"),
        "provincia": dati_visura.get("provincia"),
        "citta": dati_visura.get("citta"),
        "data_costituzione": dati_visura.get("data_costituzione"),
        "numero_dipendenti": dati_visura.get("numero_dipendenti"),
        "amministratore": dati_visura.get("amministratore")
    }

def calcola_dimensione_impresa(fatturato: float, dipendenti: int, totale_attivo: float) -> str:
    if dipendenti <= 10 and fatturato <= 2_000_000 and totale_attivo <= 2_000_000:
        return "Micro"
    elif dipendenti <= 50 and fatturato <= 10_000_000 and totale_attivo <= 10_000_000:
        return "Piccola"
    elif dipendenti <= 250 and fatturato <= 50_000_000 and totale_attivo <= 43_000_000:
        return "Media"
    else:
        return "Grande"

def calcola_indici_finanziari(dati_bilancio: dict, nome_file: str) -> dict:
    from supabase import create_client
    import os
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)
    
    fatturato = dati_bilancio.get("fatturato", 0)
    utile_netto = dati_bilancio.get("utile_netto", 0)
    ebitda = dati_bilancio.get("ebitda", 0)
    spese_rs = dati_bilancio.get("spese_ricerca_sviluppo", 0)
    costi_ambientali = dati_bilancio.get("costi_ambientali", 0)

    totale_attivo = dati_bilancio.get("totale_attivo", 1)
    disponibilita_liquide = dati_bilancio.get("disponibilita_liquide", 0)
    immobilizzazioni = dati_bilancio.get("immobilizzazioni", 0)
    indebitamento = dati_bilancio.get("indebitamento", 0)

    patrimonio_netto = dati_bilancio.get("patrimonio_netto", 1)
    attivita_correnti = dati_bilancio.get("attivita_correnti", 1)
    passivita_correnti = dati_bilancio.get("passivita_correnti", 1)
    oneri_finanziari = dati_bilancio.get("oneri_finanziari", 1)
    ammortamenti = dati_bilancio.get("ammortamenti", 0)

    investimenti_beni_strumentali = dati_bilancio.get("investimenti_beni_strumentali", 0)

    return {
        # Conto Economico
        "nome_file": nome_file,
        "fatturato_annuo": fatturato,
        "utile_netto": utile_netto,
        "ebitda": ebitda,
        "ebitda_margin": round(ebitda / fatturato, 4) if fatturato else 0,
        "spese_ricerca_sviluppo": spese_rs,
        "costi_ambientali": costi_ambientali,

        # Stato Patrimoniale
        "totale_attivo_bilancio": totale_attivo,
        "disponibilita_liquide": disponibilita_liquide,
        "immobilizzazioni_totali": immobilizzazioni,
        "indebitamento": indebitamento,
        "debt_equity_ratio": round(indebitamento / patrimonio_netto, 4) if patrimonio_netto else 0,
        "current_ratio": round(attivita_correnti / passivita_correnti, 4) if passivita_correnti else 0,
        "interest_coverage_ratio": round(ebitda / oneri_finanziari, 4) if oneri_finanziari else 0,

        # Indicatori Derivati / Strategici
        "capacita_autofinanziamento": utile_netto + ammortamenti,
        "investimenti_recenti": investimenti_beni_strumentali + spese_rs
    }

def estrai_dati_bilancio_completo(dati_visura: dict) -> dict:
    identificativi = estrai_dati_identificativi(dati_visura)
    indici = calcola_indici_finanziari(dati_visura)

    fatturato = indici.get("fatturato", 0)
    dipendenti = identificativi.get("numero_dipendenti", 0) or 0
    totale_attivo = dati_visura.get("totale_attivo", 0)

    dimensione = calcola_dimensione_impresa(fatturato, dipendenti, totale_attivo)

    return {
        **identificativi,
        **indici,
        "dimensione_impresa": dimensione,
    }
