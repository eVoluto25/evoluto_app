def simula_beneficio(bando, bilancio):
    risultato = {
        "bando": bando.get("titolo", "N/D"),
        "tipo_agevolazione": bando.get("forma_agevolazione", "N/D"),
        "investimento": bando.get("spesa_ammessa", 0),
    }

    investimento = bando.get("spesa_ammessa", 0) or 0
    fondo_perduto = 0
    credito_imposta = 0
    finanziamento = 0
    aliquota = 0.27  # ipotesi fissa

    utile_attuale = bilancio.get("utile_netto", 0) or 0
    liquidita_attuale = bilancio.get("liquidita", 0) or 0
    fatturato_attuale = bilancio.get("fatturato", 0) or 0
    ebitda = bilancio.get("ebitda", 0) or 0
    patrimonio_netto = bilancio.get("patrimonio_netto", 1) or 1  # mai zero
    debiti = bilancio.get("debiti", 0) or 0

    forma_agevolazione = bando.get("forma_agevolazione", "").lower()

    # Fondo perduto
    if "fondo perduto" in forma_agevolazione:
        fondo_perduto = investimento * 0.5  # ipotesi
        risultato["agevolazione_ottenibile"] = round(fondo_perduto, 2)
        risultato["liquidita_migliorata"] = f"+{fondo_perduto:,.0f} €"

    # Credito d’imposta
    elif "credito imposta" in forma_agevolazione or "credito d’imposta" in forma_agevolazione:
        credito_imposta = investimento * 0.4  # ipotesi
        risparmio_fiscale = credito_imposta * aliquota
        risultato["agevolazione_ottenibile"] = round(credito_imposta, 2)
        risultato["risparmio_fiscale"] = f"{risparmio_fiscale:,.0f} €"

    # Finanziamento agevolato
    elif "finanziamento" in forma_agevolazione:
        tasso = 0.01
        durata = 5
        finanziamento = investimento
        try:
            rata = (finanziamento * (tasso * (1 + tasso)**durata)) / (((1 + tasso)**durata) - 1)
        except ZeroDivisionError:
            rata = 0
        cashflow_post = ebitda - rata
        risultato["rata_annua"] = round(rata, 2)
        risultato["cashflow_post_intervento"] = f"{cashflow_post:,.0f} €"

    # Redditività simulata
    incremento_fatturato = investimento * 0.2  # ipotesi
    incremento_costi = investimento * 0.05
    utile_post = utile_attuale + incremento_fatturato - incremento_costi
    risultato["utile_atteso_post"] = f"+{utile_post:,.0f} €"

    # ROI
    roi = (incremento_fatturato - incremento_costi) / investimento if investimento else 0
    risultato["ROI"] = f"{roi*100:.1f}%"

    # Debt/Equity post
    nuovo_debito = debiti + finanziamento
    risultato["nuovo_debt_equity"] = round(nuovo_debito / patrimonio_netto, 2) if patrimonio_netto else "N/A"

    return risultato
