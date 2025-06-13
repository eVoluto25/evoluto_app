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
        den = dati.get("capitale_investito", 1)
        val = calcola_roic(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["ROIC"] = {"valore": val, "note": note}

    num = dati.get("ricavi", 0)
        den = dati.get("totale_attivo", 1)
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
        indici["EBIT OF"] = {"valore": val, "note": note}

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
        indici["PFNPN"] = {"valore": val, "note": note}

    num = dati.get("patrimonio_netto", 0)
        den = dati.get("totale_fonti", 1)
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

    num = dati.get("cap_medio_termine", 0)
        den = dati.get("immobilizzazioni", 1)
        val = calcola_copertura_imm(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["COPERTURA IMM"] = {"valore": val, "note": note}

    num = dati.get("liquidita_imm", 0)
        den = dati.get("debiti_brevedurata", 1)
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

    num = dati.get("liquidita_imm", 0)
        den = dati.get("passivo_corr", 1)
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

    num = dati.get("attivo_corr", 0)
        den = dati.get("passivo_corr", 1)
        val = calcola_mcc(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["MCC"] = {"valore": val, "note": note}

    num = dati.get("cash_flow_operativo", 0)
        den = dati.get("quota_debiti", 1)
        val = calcola_dscr(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["DSCR"] = {"valore": val, "note": note}

    num = dati.get("cash_flow_operativo", 0)
        den = dati.get("debiti", 1)
        val = calcola_cashflow_debiti(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["CASHFLOW DEBITI"] = {"valore": val, "note": note}

    num = dati.get("disponibilita", 0)
        den = dati.get("passivo_corr", 1)
        val = calcola_liquidita_immediata(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["LIQUIDITA IMMEDIATA"] = {"valore": val, "note": note}

    num = dati.get("liquidita_imm", 0)
        den = dati.get("passivo_corr", 1)
        val = calcola_acid_test(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["ACID TEST"] = {"valore": val, "note": note}

    num = dati.get("ebitda", 0)
        den = dati.get("oneri_fin", 1)
        val = calcola_coverage_ratio(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["COVERAGE RATIO"] = {"valore": val, "note": note}

    num = dati.get("cash_flow_operativo", 0)
        den = dati.get("ricavi", 1)
        val = calcola_cf_ricavi(num, den)
        if den == 0:
            note = "Denominatore assente o zero"
        elif val < 0:
            note = f"Valore negativo – Numeratore: {num}, Denominatore: {den}"
        else:
            note = f"Numeratore: {num}, Denominatore: {den}"
        indici["CF RICAVI"] = {"valore": val, "note": note}

    num = dati.get("cash_flow_operativo", 0)
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

    num = dati.get("capitale_netto", 0)
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
        indici["RIGIDITA INV"] = {"valore": val, "note": note}

    num = dati.get("patrimonio_netto", 0)
        den = dati.get("totale_passivo", 1)
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
        crisi = crescita = espansione = 0

        if indici.get("Debt/Equity") is not None and 0.5 <= indici["Debt/Equity"] <= 2:
            crisi += 1
        if indici.get("EBITDA Margin", 0) > 0:
            crisi += 1
        if indici.get("Risultato Netto", 0) > 0:
            crisi += 1

        if indici.get("Autofinanziamento", False):
            crescita += 1
        if indici.get("Solidità patrimoniale", False):
            crescita += 1
        if indici.get("Investimenti presenti", False):
            crescita += 1

        if indici.get("Fatturato in crescita", False):
            espansione += 1
        if indici.get("ROS", 0) > 0.05:
            espansione += 1
        if indici.get("EBITDA Margin", 0) > 0.1:
            espansione += 1

        logging.info(f"Punteggi: Crisi={crisi}, Crescita={crescita}, Espansione={espansione}")

        if crisi == crescita == espansione:
            if espansione > 0:
                return "Espansione"
            elif crescita > 0:
                return "Crescita"
            else:
                return "Crisi"

        punteggi = {"Crisi": crisi, "Crescita": crescita, "Espansione": espansione}
        return max(punteggi, key=punteggi.get)

    except Exception as e:
        logging.error(f"Errore durante l'assegnazione della macro area: {e}")
        return "ND"
