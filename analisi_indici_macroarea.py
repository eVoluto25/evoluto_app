from formule_indici import *
import logging

def calcola_indici(dati):
    indici = {}
    indici["ROE"] = calcola_roe(dati.get("Risultato Netto", 0), dati.get("Patrimonio Netto", 1))
    indici["ROI"] = calcola_roi(dati.get("EBITDA", 0), dati.get("Totale Attivo", 1))
    indici["ROS"] = calcola_ros(dati.get("EBITDA", 0), dati.get("Ricavi", 1))
    indici["ROIC"] = calcola_roic(dati.get("EBITDA", 0), dati.get("Debiti", 1))
    indici["ROT"] = calcola_rot(dati.get("Ricavi", 0), dati.get("Totale Attivo", 1))
    indici["EBITDA MARGIN"] = calcola_ebitda_margin(dati.get("EBITDA", 0), dati.get("Ricavi", 1))
    indici["EBIT/OF"] = calcola_ebit_of(dati.get("EBITDA", 0), dati.get("Oneri Finanziari", 1))
    indici["LEVERAGE"] = calcola_leverage(dati.get("Totale Passivo", 0), dati.get("Patrimonio Netto", 1))
    indici["DEBT EQUITY"] = calcola_debt_equity(dati.get("Debiti", 0), dati.get("Patrimonio Netto", 1))
    indici["PFN/PN"] = calcola_pfnpn(dati.get("PFN", 0), dati.get("Patrimonio Netto", 1))
    indici["INDIPENDENZA FIN"] = calcola_indipendenza_fin(dati.get("Patrimonio Netto", 0), dati.get("Totale Passivo", 1))
    indici["MARGINE STRUTTURA"] = calcola_margine_struttura(dati.get("Patrimonio Netto", 0), dati.get("Immobilizzazioni", 1))
    indici["COPERTURA IMM"] = calcola_copertura_imm(dati.get("Patrimonio Netto", 0), dati.get("Immobilizzazioni", 1))
    indici["MARGINE TESORERIA"] = calcola_margine_tesoreria(dati.get("Disponibilità liquide", 0), dati.get("Passivo Corrente", 1))
    indici["CCN"] = calcola_ccn(dati.get("Attivo Corrente", 0), dati.get("Passivo Corrente", 1))
    indici["QUICK RATIO"] = calcola_quick_ratio(dati.get("Disponibilità liquide", 0), dati.get("Passivo Corrente", 1))
    indici["CURRENT RATIO"] = calcola_current_ratio(dati.get("Attivo Corrente", 0), dati.get("Passivo Corrente", 1))
    indici["MCC"] = calcola_mcc(dati.get("Attivo Corrente", 0), dati.get("Passivo Corrente", 1))
    indici["DSCR"] = calcola_dscr(dati.get("Cash Flow Operativo", 0), dati.get("Quota Debiti", 1))
    indici["CASHFLOW DEBITI"] = calcola_cashflow_debiti(dati.get("Cash Flow Operativo", 0), dati.get("Debiti", 1))
    indici["LIQUIDITÀ IMMEDIATA"] = calcola_liquidita_immediata(dati.get("Disponibilità liquide", 0), dati.get("Passivo Corrente", 1))
    indici["ACID TEST"] = calcola_acid_test(dati.get("Disponibilità liquide", 0), dati.get("Passivo Corrente", 1))
    indici["COVERAGE RATIO"] = calcola_coverage_ratio(dati.get("EBITDA", 0), dati.get("Oneri Finanziari", 1))
    indici["CF RICAVI"] = calcola_cf_ricavi(dati.get("Cash Flow Operativo", 0), dati.get("Ricavi", 1))
    indici["CF ATTIVO"] = calcola_cf_attivo(dati.get("Cash Flow Operativo", 0), dati.get("Totale Attivo", 1))
    indici["ATT CORR ATTIVO"] = calcola_att_corr_attivo(dati.get("Attivo Corrente", 0), dati.get("Totale Attivo", 1))
    indici["ONERI RICAVI"] = calcola_oneri_ricavi(dati.get("Oneri Finanziari", 0), dati.get("Ricavi", 1))
    indici["ROA"] = calcola_roa(dati.get("Risultato Netto", 0), dati.get("Totale Attivo", 1))
    indici["CAP NETTO ATTIVO"] = calcola_cap_netto_attivo(dati.get("Patrimonio Netto", 0), dati.get("Totale Attivo", 1))
    indici["RIGIDITÀ INV"] = calcola_rigidita_inv(dati.get("Immobilizzazioni", 0), dati.get("Totale Attivo", 1))
    indici["AUTONOMIA FINANZIARIA"] = calcola_autonomia_finanziaria(dati.get("Patrimonio Netto", 0), dati.get("Totale Passivo", 1))
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
