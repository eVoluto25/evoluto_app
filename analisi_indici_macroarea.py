import logging

def calcola_indici(dati):
    indici = {}

    def safe_div(num, den):
        try:
            return round(num / den, 6) if num is not None and den not in (None, 0) else "ND"
        except:
            return "ND"

    ricavi = dati.get("Ricavi")
    utile = dati.get("Risultato Netto")
    patrimonio = dati.get("Patrimonio Netto")
    debiti = dati.get("Debiti")
    attivo = dati.get("Totale Attivo")
    passivo = dati.get("Totale Passivo")
    liquidita = dati.get("Disponibilità liquide")
    rimanenze = dati.get("Rimanenze")
    ebitda = dati.get("EBITDA")
    immobilizzazioni = dati.get("Immobilizzazioni")
    oneri_fin = dati.get("Oneri Finanziari")

    indici["ROE"] = safe_div(utile, patrimonio)
    indici["Leverage"] = safe_div(passivo, patrimonio)
    indici["Margine di Struttura"] = safe_div(patrimonio, immobilizzazioni)
    indici["Indipendenza Finanziaria"] = safe_div(patrimonio, attivo)
    indici["PFN/PN"] = safe_div((debiti or 0) - (liquidita or 0), patrimonio)
    indici["EBIT/OF"] = safe_div(ebitda, oneri_fin)
    indici["Capitale Circolante Netto"] = round((liquidita or 0) + (rimanenze or 0) - (debiti or 0), 2)

    # Indici placeholder
    for k in [
        "ROI", "ROS", "ROT", "ROIC", "Copertura Immobilizzazioni", "Current Ratio", "Quick Ratio",
        "Margine di Tesoreria", "MOL/PFN", "Flusso di Cassa / OF", "PFN/MOL", "PFN/Ricavi",
        "Cash Wallet Risk Index", "Collateral Distortion Index", "Sconfinamento Medio",
        "Tensione Finanziaria", "Cash Wallet Management Index", "Duration"
    ]:
        indici[k] = "ND"

    return indici

def assegna_macro_area(indici):
    try:
        crisi = 0
        crescita = 0
        espansione = 0

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
