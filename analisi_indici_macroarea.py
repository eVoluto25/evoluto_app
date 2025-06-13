from formule_indici import *
import logging
import json

def calcola_indici(dati):
    indici = 

    # Mappatura variabili in base al file alias
    try:
        with open("mappa_alias_variabili.json") as f:
            alias = json.load(f)
        dati = {alias.get(k, k): v for k, v in dati.items()}
    except Exception as e:
        logging.warning(f"Alias mapping non applicato: {e}")

    num = dati.get("utile_netto", 0)
    den = dati.get("patrimonio_netto", 1)
    val = calcola_roe(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROE"] = {"valore": val, "note": note}

    num = dati.get("ebit", 0)
    den = dati.get("totale_attivo", 1)
    val = calcola_roi(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROI"] = {"valore": val, "note": note}

    num = dati.get("ebit", 0)
    den = dati.get("ricavi", 1)
    val = calcola_ros(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROS"] = {"valore": val, "note": note}

    num = dati.get("ebit", 0)
    den = dati.get("debiti", 1)
    val = calcola_roic(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROIC"] = {"valore": val, "note": note}

    num = dati.get("ricavi", 0)
    den = dati.get("attivo", 1)
    val = calcola_rot(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROT"] = {"valore": val, "note": note}

    num = dati.get("ebitda", 0)
    den = dati.get("ricavi", 1)
    val = calcola_ebitda_margin(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["EBITDA MARGIN"] = {"valore": val, "note": note}

    num = dati.get("ebit", 0)
    den = dati.get("oneri_fin", 1)
    val = calcola_ebit_of(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["EBIT/OF"] = {"valore": val, "note": note}

    num = dati.get("totale_passivo", 0)
    den = dati.get("patrimonio_netto", 1)
    val = calcola_leverage(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["LEVERAGE"] = {"valore": val, "note": note}

    num = dati.get("debiti", 0)
    den = dati.get("patrimonio_netto", 1)
    val = calcola_debt_equity(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["DEBT EQUITY"] = {"valore": val, "note": note}

    num = dati.get("pfn", 0)
    den = dati.get("patrimonio_netto", 1)
    val = calcola_pfnpn(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["PFN/PN"] = {"valore": val, "note": note}

    num = dati.get("patrimonio_netto", 0)
    den = dati.get("totale_attivo", 1)
    val = calcola_indipendenza_fin(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["INDIPENDENZA FIN"] = {"valore": val, "note": note}

    num = dati.get("patrimonio_netto", 0)
    den = dati.get("immobilizzazioni", 1)
    val = calcola_margine_struttura(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["MARGINE STRUTTURA"] = {"valore": val, "note": note}

    num = dati.get("patrimonio_netto", 0)
    den = dati.get("immobilizzazioni", 1)
    val = calcola_copertura_imm(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["COPERTURA IMM"] = {"valore": val, "note": note}

    num = dati.get("liquidita", 0)
    den = dati.get("passivo_corr", 1)
    val = calcola_margine_tesoreria(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["MARGINE TESORERIA"] = {"valore": val, "note": note}

    num = dati.get("attivo_corr", 0)
    den = dati.get("passivo_corr", 1)
    val = calcola_ccn(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CCN"] = {"valore": val, "note": note}

    num = dati.get("attivo_corr", 0)
    den = dati.get("rimanenze", 1)
    val = calcola_quick_ratio(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["QUICK RATIO"] = {"valore": val, "note": note}

    num = dati.get("attivo_corr", 0)
    den = dati.get("passivo_corr", 1)
    val = calcola_current_ratio(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CURRENT RATIO"] = {"valore": val, "note": note}

    num = dati.get("ebit", 0)
    den = dati.get("oneri_fin", 1)
    val = calcola_mcc(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["MCC"] = {"valore": val, "note": note}

    num = dati.get("flussi_cassa", 0)
    den = dati.get("rata_debiti", 1)
    val = calcola_dscr(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["DSCR"] = {"valore": val, "note": note}

    num = dati.get("flussi_cassa", 0)
    den = dati.get("debiti", 1)
    val = calcola_cashflow_debiti(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CASHFLOW DEBITI"] = {"valore": val, "note": note}

    num = dati.get("liquidita", 0)
    den = dati.get("passivo_corr", 1)
    val = calcola_liquidita_immediata(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["LIQUIDITÀ IMMEDIATA"] = {"valore": val, "note": note}

    num = dati.get("liquidita", 0)
    den = dati.get("passivo_corr", 1)
    val = calcola_acid_test(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ACID TEST"] = {"valore": val, "note": note}

    num = dati.get("ebit", 0)
    den = dati.get("oneri_fin", 1)
    val = calcola_coverage_ratio(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["COVERAGE RATIO"] = {"valore": val, "note": note}

    num = dati.get("flussi_cassa", 0)
    den = dati.get("ricavi", 1)
    val = calcola_cf_ricavi(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CF RICAVI"] = {"valore": val, "note": note}

    num = dati.get("flussi_cassa", 0)
    den = dati.get("totale_attivo", 1)
    val = calcola_cf_attivo(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CF ATTIVO"] = {"valore": val, "note": note}

    num = dati.get("attivo_corr", 0)
    den = dati.get("totale_attivo", 1)
    val = calcola_att_corr_attivo(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ATT CORR ATTIVO"] = {"valore": val, "note": note}

    num = dati.get("oneri_fin", 0)
    den = dati.get("ricavi", 1)
    val = calcola_oneri_ricavi(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ONERI RICAVI"] = {"valore": val, "note": note}

    num = dati.get("utile_netto", 0)
    den = dati.get("totale_attivo", 1)
    val = calcola_roa(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROA"] = {"valore": val, "note": note}

    num = dati.get("patrimonio_netto", 0)
    den = dati.get("totale_attivo", 1)
    val = calcola_cap_netto_attivo(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CAP NETTO ATTIVO"] = {"valore": val, "note": note}

    num = dati.get("immobilizzazioni", 0)
    den = dati.get("totale_attivo", 1)
    val = calcola_rigidita_inv(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["RIGIDITÀ INV"] = {"valore": val, "note": note}

    num = dati.get("patrimonio_netto", 0)
    den = dati.get("totale_attivo", 1)
    val = calcola_autonomia_finanziaria(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["AUTONOMIA FINANZIARIA"] = {"valore": val, "note": note}

    return indici

def assegna_macro_area(indici: dict) -> str:
    try:
        roe = indici['ROE']['valore']
        pfn_pn = indici['PFN/PN']['valore']
        leverage = indici['LEVERAGE']['valore']
        oneri_ricavi = indici['ONERI RICAVI']['valore']
        dscr = indici['DSCR']['valore']
        coverage = indici['COVERAGE RATIO']['valore']

        if roe > 0.08 and pfn_pn < 1 and leverage < 4 and oneri_ricavi < 0.2 and dscr > 1 and coverage > 1:
            return "Espansione"
        elif roe < 0 or pfn_pn > 1.5 or leverage > 5 or oneri_ricavi > 0.4 or dscr < 0.8 or coverage < 0.8:
            return "Crisi"
        else:
            return "Stabilità"
    except Exception as e:
        logging.error(f'Errore nell\'assegnazione macro area: {e}')
        return "Non Determinato"
