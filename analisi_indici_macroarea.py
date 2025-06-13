import logging
from formule_indici import calcola_indici_finanziari

def calcola_indici(dati):
    indici = {}

    # Estrazione variabili base
    utile = dati.get("Risultato Netto")
    ricavi = dati.get("Ricavi")
    patrimonio = dati.get("Patrimonio Netto")
    attivo = dati.get("Totale Attivo")
    passivo = dati.get("Totale Passivo")
    liquidita = dati.get("Disponibilità liquide")
    debiti = dati.get("Debiti")
    rimanenze = dati.get("Rimanenze")
    immobilizzazioni = dati.get("Immobilizzazioni")
    oneri_fin = dati.get("Oneri Finanziari")
    ebit = dati.get("EBIT") or dati.get("EBITDA")  # fallback proxy
    attivo_corr = dati.get("Attivo Corrente")
    passivo_corr = dati.get("Passivo Corrente")

    # Calcolo indici reali
    indici["ROE"] = calcola_roe(utile, patrimonio)
    indici["ROI"] = calcola_roi(ebit, attivo)
    indici["ROS"] = calcola_ros(ebit, ricavi)
    indici["ROIC"] = calcola_roic(ebit, debiti, patrimonio)
    indici["ROT"] = calcola_rot(ricavi, attivo)
    indici["Leverage"] = calcola_leverage(passivo, patrimonio)
    indici["PFN/PN"] = calcola_pfnpn(debiti, liquidita, patrimonio)
    indici["EBIT/OF"] = calcola_ebit_of(ebit, oneri_fin)
    indici["Current Ratio"] = calcola_current_ratio(attivo_corr, passivo_corr)
    indici["Quick Ratio"] = calcola_quick_ratio(attivo_corr, rimanenze, passivo_corr)
    indici["Indipendenza Finanziaria"] = calcola_indipendenza_fin(patrimonio, attivo)
    indici["Margine di Tesoreria"] = calcola_margine_tesoreria(liquidita, passivo_corr)
    indici["Copertura Immobilizzazioni"] = calcola_copertura_imm(patrimonio, immobilizzazioni)
    indici["Margine di Struttura"] = calcola_margine_struttura(patrimonio, immobilizzazioni)
    indici["Capitale Circolante Netto"] = calcola_ccn(attivo_corr, passivo_corr)
    indici["Debt/Equity"] = calcola_debt_equity(debiti, patrimonio)
    indici["EBITDA Margin"] = calcola_ebitda_margin(ebitda, ricavi)
    indici["Interest Coverage"] = calcola_interest_coverage(ebitda, oneri_fin)
    indici["Z-Score Altman"] = calcola_zscore_altman(ebitda, patrimonio, utile, attivo_corr, passivo_corr, ricavi, attivo)
    indici["DSCR"] = calcola_dscr(ebitda, dati.get("Quota Debito Annua", 0))
    indici["Leverage"] = calcola_leverage(attivo, patrimonio)
    indici["Indipendenza Finanziaria"] = calcola_indipendenza_fin(patrimonio, passivo)
    indici["Copertura Immobilizzazioni"] = calcola_copertura_imm(patrimonio, dati.get("Debiti M/L Termine", 0), dati.get("Immobilizzazioni", 0))
    indici["Classe MCC"] = calcola_classe_mcc(indici)  

    return indici

def assegna_macro_area(indici):
    try:
        crisi = crescita = espansione = 0

        roe = indici.get("ROE")
        leverage = indici.get("Leverage")
        struttura = indici.get("Margine di Struttura")

        if isinstance(roe, float) and roe < 0.01:
            crisi += 1
        if isinstance(leverage, float) and leverage > 4:
            crisi += 1
        if isinstance(struttura, float) and struttura < 0.8:
            crisi += 1

        if isinstance(roe, float) and roe > 0.05:
            crescita += 1
        if isinstance(struttura, float) and struttura > 1:
            crescita += 1

        if isinstance(roe, float) and roe > 0.1:
            espansione += 1
        if isinstance(leverage, float) and leverage < 2:
            espansione += 1

        logging.info(f"Punteggi: Crisi={crisi}, Crescita={crescita}, Espansione={espansione}")

        if espansione >= 2:
            return "Espansione"
        elif crescita >= 2:
            return "Crescita"
        else:
            return "Crisi"

    except Exception as e:
        logging.error(f"Errore durante l'assegnazione della macro area: {e}")
        return "ND"
