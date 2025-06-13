from formule_indici import *
import logging

def calcola_indici(dati):
    indici = {}
    indici["ROE"] = calcola_roe(dati.get("utile_netto", 0), dati.get("patrimonio_netto", 1))
    indici["ROI"] = calcola_roi(dati.get("ebit", 0), dati.get("totale_attivo", 1))
    indici["ROS"] = calcola_ros(dati.get("ebit", 0), dati.get("ricavi", 1))
    indici["ROIC"] = calcola_roic(dati.get("ebit", 0), dati.get("capitale_investito", 1))
    indici["ROT"] = calcola_rot(dati.get("ricavi", 0), dati.get("totale_attivo", 1))
    indici["EBITDA MARGIN"] = calcola_ebitda_margin(dati.get("ebitda", 0), dati.get("ricavi", 1))
    indici["EBIT OF"] = calcola_ebit_of(dati.get("ebit", 0), dati.get("oneri_fin", 1))
    indici["LEVERAGE"] = calcola_leverage(dati.get("totale_passivo", 0), dati.get("patrimonio_netto", 1))
    indici["DEBT EQUITY"] = calcola_debt_equity(dati.get("debiti", 0), dati.get("patrimonio_netto", 1))
    indici["PFNPN"] = calcola_pfnpn(dati.get("pfn", 0), dati.get("patrimonio_netto", 1))
    indici["INDIPENDENZA FIN"] = calcola_indipendenza_fin(dati.get("patrimonio_netto", 0), dati.get("totale_fonti", 1))
    indici["MARGINE STRUTTURA"] = calcola_margine_struttura(dati.get("patrimonio_netto", 0), dati.get("immobilizzazioni", 1))
    indici["COPERTURA IMM"] = calcola_copertura_imm(dati.get("cap_medio_termine", 0), dati.get("immobilizzazioni", 1))
    indici["MARGINE TESORERIA"] = calcola_margine_tesoreria(dati.get("liquidita_imm", 0), dati.get("debiti_brevedurata", 1))
    indici["CCN"] = calcola_ccn(dati.get("attivo_corr", 0), dati.get("passivo_corr", 1))
    indici["QUICK RATIO"] = calcola_quick_ratio(dati.get("liquidita_imm", 0), dati.get("passivo_corr", 1))
    indici["CURRENT RATIO"] = calcola_current_ratio(dati.get("attivo_corr", 0), dati.get("passivo_corr", 1))
    indici["MCC"] = calcola_mcc(dati.get("attivo_corr", 0), dati.get("passivo_corr", 1))
    indici["DSCR"] = calcola_dscr(dati.get("cash_flow_operativo", 0), dati.get("quota_debiti", 1))
    indici["CASHFLOW DEBITI"] = calcola_cashflow_debiti(dati.get("cash_flow_operativo", 0), dati.get("debiti", 1))
    indici["LIQUIDITA IMMEDIATA"] = calcola_liquidita_immediata(dati.get("disponibilita", 0), dati.get("passivo_corr", 1))
    indici["ACID TEST"] = calcola_acid_test(dati.get("liquidita_imm", 0), dati.get("passivo_corr", 1))
    indici["COVERAGE RATIO"] = calcola_coverage_ratio(dati.get("ebitda", 0), dati.get("oneri_fin", 1))
    indici["CF RICAVI"] = calcola_cf_ricavi(dati.get("cash_flow_operativo", 0), dati.get("ricavi", 1))
    indici["CF ATTIVO"] = calcola_cf_attivo(dati.get("cash_flow_operativo", 0), dati.get("totale_attivo", 1))
    indici["ATT CORR ATTIVO"] = calcola_att_corr_attivo(dati.get("attivo_corr", 0), dati.get("totale_attivo", 1))
    indici["ONERI RICAVI"] = calcola_oneri_ricavi(dati.get("oneri_fin", 0), dati.get("ricavi", 1))
    indici["ROA"] = calcola_roa(dati.get("utile_netto", 0), dati.get("totale_attivo", 1))
    indici["CAP NETTO ATTIVO"] = calcola_cap_netto_attivo(dati.get("capitale_netto", 0), dati.get("totale_attivo", 1))
    indici["RIGIDITA INV"] = calcola_rigidita_inv(dati.get("immobilizzazioni", 0), dati.get("totale_attivo", 1))
    indici["AUTONOMIA FINANZIARIA"] = calcola_autonomia_finanziaria(dati.get("patrimonio_netto", 0), dati.get("totale_passivo", 1))
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
