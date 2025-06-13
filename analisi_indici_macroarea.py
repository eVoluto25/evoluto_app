from formule_indici import (
    calcola_roe,
    calcola_roi,
    calcola_ros,
    calcola_roic,
    calcola_roa,
    calcola_ebitda_margin,
    calcola_ebit_of,
    calcola_leverage,
    calcola_debt_equity,
    calcola_pfnpn,
    calcola_indipendenza,
    calcola_margine_struttura,
    calcola_copertura_imm,
    calcola_margine_tesoreria,
    calcola_ccn,
    calcola_quick_ratio,
    calcola_current_ratio,
    calcola_mcc,
    calcola_dscr,
    calcola_cashflow_debiti,
    calcola_coverage,
    calcola_cf_ricavi,
    calcola_cf_attivo,
    calcola_att_corr,
    calcola_oneri_ricavi,
    calcola_cap_netto_attivo,
    calcola_rigidita,
    calcola_autonomia
)
import logging
import json
import os

def calcola_indici(dati):
    indici = {}

    # Mappatura variabili in base al file alias
    try:
        alias_path = os.path.join(os.path.dirname(__file__), "mappa_alias_variabili.json")
        with open(alias_path) as f:
            alias = json.load(f)
            dati = {alias.get(k, k): v for k, v in dati.items()}
    except Exception as e:
        logging.warning(f"Alias mapping non applicato: {e}")

    def assegna(nome, num, den, formula):
        try:
            if den == 0:
                note = f"Denominatore assente o zero"
                val = 0.0
            else:
                val = formula(num, den)
                if val < 0:
                    note = f"⚠️Valore negativo – Numeratore: {num}, Denominatore: {den}"
                else:
                    note = f"✅Numeratore: {num}, Denominatore: {den}"
            indici[nome] = {"valore": val, "note": note}
        except Exception as e:
            logging.warning(f"Errore calcolo indice {nome}: {e}")
            indici[nome] = {"valore": 0.0, "note": f"Errore calcolo: {e}"}

    # Indici da calcolare
    assegna("ROE", dati.get("utile_netto", 0), dati.get("patrimonio_netto", 1), calcola_roe)
    assegna("ROI", dati.get("utile_netto", 0), dati.get("totale_attivo", 1), calcola_roi)
    assegna("ROS", dati.get("utile_netto", 0), dati.get("ricavi", 1), calcola_ros)
    assegna("ROIC", dati.get("utile_netto", 0), dati.get("debiti", 1), calcola_roic)
    assegna("ROA", dati.get("utile_netto", 0), dati.get("totale_attivo", 1), calcola_roa)

    assegna("EBITDA MARGIN", dati.get("ebitda", 0), dati.get("ricavi", 1), calcola_ebitda_margin)
    assegna("EBIT/OF", dati.get("ebit", 0), dati.get("oneri_fin", 1), calcola_ebit_of)
    assegna("LEVERAGE", dati.get("totale_attivo", 0), dati.get("patrimonio_netto", 1), calcola_leverage)
    assegna("DEBT EQUITY", dati.get("debiti", 0), dati.get("patrimonio_netto", 1), calcola_debt_equity)
    assegna("PFN/PN", dati.get("pfn", 0), dati.get("patrimonio_netto", 1), calcola_pfnpn)
    assegna("INDIPENDENZA FIN", dati.get("patrimonio_netto", 0), dati.get("totale_attivo", 1), calcola_indipendenza)

    assegna("MARGINE STRUTTURA", dati.get("patrimonio_netto", 0), dati.get("immobilizzazioni", 1), calcola_margine_struttura)
    assegna("COPERTURA IMM", dati.get("patrimonio_netto", 0), dati.get("immobilizzazioni", 1), calcola_copertura_imm)
    assegna("MARGINE TESORERIA", dati.get("liquidita", 0), dati.get("passivo_corr", 1), calcola_margine_tesoreria)
    assegna("CCN", dati.get("attivo_corr", 0), dati.get("passivo_corr", 1), calcola_ccn)
    assegna("QUICK RATIO", dati.get("liquidita", 0), dati.get("passivo_corr", 1), calcola_quick_ratio)
    assegna("CURRENT RATIO", dati.get("attivo_corr", 0), dati.get("passivo_corr", 1), calcola_current_ratio)

    assegna("MCC", dati.get("utile_netto", 0), dati.get("oneri_fin", 1), calcola_mcc)
    assegna("DSCR", dati.get("utile_netto", 0), dati.get("oneri_fin", 1), calcola_dscr)
    assegna("CASHFLOW DEBITI", dati.get("utile_netto", 0), dati.get("debiti", 1), calcola_cashflow_debiti)
    assegna("LIQUIDITÀ IMMEDIATA", dati.get("liquidita", 0), 1, lambda x, y: x)
    assegna("ACID TEST", dati.get("liquidita", 0), dati.get("passivo_corr", 1), calcola_quick_ratio)
    assegna("COVERAGE RATIO", dati.get("utile_netto", 0), dati.get("oneri_fin", 1), calcola_coverage)

    assegna("CF RICAVI", dati.get("utile_netto", 0), dati.get("ricavi", 1), calcola_cf_ricavi)
    assegna("CF ATTIVO", dati.get("utile_netto", 0), dati.get("totale_attivo", 1), calcola_cf_attivo)
    assegna("ATT CORR ATTIVO", dati.get("attivo_corr", 0), dati.get("totale_attivo", 1), calcola_att_corr)
    assegna("ONERI RICAVI", dati.get("oneri_fin", 0), dati.get("ricavi", 1), calcola_oneri_ricavi)

    assegna("CAP NETTO ATTIVO", dati.get("patrimonio_netto", 0), dati.get("totale_attivo", 1), calcola_cap_netto_attivo)
    assegna("RIGIDITÀ INV", dati.get("immobilizzazioni", 0), dati.get("totale_attivo", 1), calcola_rigidita)
    assegna("AUTONOMIA FINANZIARIA", dati.get("patrimonio_netto", 0), dati.get("totale_attivo", 1), calcola_autonomia)

    logging.info(f"Indici calcolati: {indici}")
    return indici
