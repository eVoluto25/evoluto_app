from formule_indici import *
import logging

def calcola_indici(dati):
    indici = {}

    num = dati.get("Risultato Netto", 0)
    den = dati.get("Patrimonio Netto", 1)
    val = calcola_roe(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROE"] = {"valore": val, "note": note}

    num = dati.get("EBITDA", 0)
    den = dati.get("Totale Attivo", 1)
    val = calcola_roi(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROI"] = {"valore": val, "note": note}

    num = dati.get("EBITDA", 0)
    den = dati.get("Ricavi", 1)
    val = calcola_ros(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROS"] = {"valore": val, "note": note}

    num = dati.get("EBITDA", 0)
    den = dati.get("Capitale Netto", 1)
    val = calcola_roic(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROIC"] = {"valore": val, "note": note}

    num = dati.get("Ricavi", 0)
    den = dati.get("Totale Attivo", 1)
    val = calcola_rot(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROT"] = {"valore": val, "note": note}

    num = dati.get("EBITDA", 0)
    den = dati.get("Ricavi", 1)
    val = calcola_ebitda_margin(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["EBITDA MARGIN"] = {"valore": val, "note": note}

    num = dati.get("EBITDA", 0)
    den = dati.get("Oneri Finanziari", 1)
    val = calcola_ebit/of(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["EBIT/OF"] = {"valore": val, "note": note}

    num = dati.get("Totale Attivo", 0)
    den = dati.get("Patrimonio Netto", 1)
    val = calcola_leverage(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["LEVERAGE"] = {"valore": val, "note": note}

    num = dati.get("Debiti", 0)
    den = dati.get("Patrimonio Netto", 1)
    val = calcola_debt_equity(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["DEBT EQUITY"] = {"valore": val, "note": note}

    num = dati.get("PFN", 0)
    den = dati.get("Patrimonio Netto", 1)
    val = calcola_pfn/pn(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["PFN/PN"] = {"valore": val, "note": note}

    num = dati.get("Patrimonio Netto", 0)
    den = dati.get("Totale Passivo", 1)
    val = calcola_indipendenza_fin(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["INDIPENDENZA FIN"] = {"valore": val, "note": note}

    num = dati.get("Patrimonio Netto", 0)
    den = dati.get("Immobilizzazioni", 1)
    val = calcola_margine_struttura(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["MARGINE STRUTTURA"] = {"valore": val, "note": note}

    num = dati.get("Patrimonio Netto", 0)
    den = dati.get("Immobilizzazioni", 1)
    val = calcola_copertura_imm(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["COPERTURA IMM"] = {"valore": val, "note": note}

    num = dati.get("Disponibilità liquide", 0)
    den = dati.get("Passivo Corrente", 1)
    val = calcola_margine_tesoreria(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["MARGINE TESORERIA"] = {"valore": val, "note": note}

    num = dati.get("Attivo Corrente", 0)
    den = dati.get("Passivo Corrente", 1)
    val = calcola_ccn(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CCN"] = {"valore": val, "note": note}

    num = dati.get("Disponibilità liquide", 0)
    den = dati.get("Passivo Corrente", 1)
    val = calcola_quick_ratio(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["QUICK RATIO"] = {"valore": val, "note": note}

    num = dati.get("Attivo Corrente", 0)
    den = dati.get("Passivo Corrente", 1)
    val = calcola_current_ratio(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CURRENT RATIO"] = {"valore": val, "note": note}

    num = dati.get("Cash Flow Operativo", 0)
    den = dati.get("Quota Debiti", 1)
    val = calcola_mcc(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["MCC"] = {"valore": val, "note": note}

    num = dati.get("Cash Flow Operativo", 0)
    den = dati.get("Quota Debiti", 1)
    val = calcola_dscr(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["DSCR"] = {"valore": val, "note": note}

    num = dati.get("Cash Flow Operativo", 0)
    den = dati.get("Debiti", 1)
    val = calcola_cashflow_debiti(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CASHFLOW DEBITI"] = {"valore": val, "note": note}

    num = dati.get("Disponibilità liquide", 0)
    den = dati.get("Passivo Corrente", 1)
    val = calcola_liquidità_immediata(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["LIQUIDITÀ IMMEDIATA"] = {"valore": val, "note": note}

    num = dati.get("Disponibilità liquide", 0)
    den = dati.get("Passivo Corrente", 1)
    val = calcola_acid_test(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ACID TEST"] = {"valore": val, "note": note}

    num = dati.get("EBITDA", 0)
    den = dati.get("Oneri Finanziari", 1)
    val = calcola_coverage_ratio(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["COVERAGE RATIO"] = {"valore": val, "note": note}

    num = dati.get("Cash Flow Operativo", 0)
    den = dati.get("Ricavi", 1)
    val = calcola_cf_ricavi(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CF RICAVI"] = {"valore": val, "note": note}

    num = dati.get("Cash Flow Operativo", 0)
    den = dati.get("Totale Attivo", 1)
    val = calcola_cf_attivo(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CF ATTIVO"] = {"valore": val, "note": note}

    num = dati.get("Attivo Corrente", 0)
    den = dati.get("Totale Attivo", 1)
    val = calcola_att_corr_attivo(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ATT CORR ATTIVO"] = {"valore": val, "note": note}

    num = dati.get("Oneri Finanziari", 0)
    den = dati.get("Ricavi", 1)
    val = calcola_oneri_ricavi(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ONERI RICAVI"] = {"valore": val, "note": note}

    num = dati.get("Risultato Netto", 0)
    den = dati.get("Totale Attivo", 1)
    val = calcola_roa(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["ROA"] = {"valore": val, "note": note}

    num = dati.get("Patrimonio Netto", 0)
    den = dati.get("Totale Attivo", 1)
    val = calcola_cap_netto_attivo(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["CAP NETTO ATTIVO"] = {"valore": val, "note": note}

    num = dati.get("Immobilizzazioni", 0)
    den = dati.get("Totale Attivo", 1)
    val = calcola_rigidità_inv(num, den)
    if den == 0:
        note = "Denominatore assente o zero"
    elif val < 0:
        note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
    else:
        note = f"Numeratore: {num}, Denominatore: {den}"
    indici["RIGIDITÀ INV"] = {"valore": val, "note": note}

    num = dati.get("Patrimonio Netto", 0)
    den = dati.get("Totale Passivo", 1)
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