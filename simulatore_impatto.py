def simula_beneficio(bando, bilancio):
    # Dati iniziali dal bando
    titolo = bando.get("titolo", "N/D")
    tipo_agevolazione = bando.get("forma_agevolazione", "N/D")
    investimento = bando.get("spesa_ammessa", 0) or 0

    # Dati di bilancio
    utile = bilancio.get("utile_netto", 0) or 0
    liquidita = bilancio.get("liquidità", 0) or 0
    fatturato = bilancio.get("fatturato", 0) or 0
    ebitda = bilancio.get("ebitda", 0) or 0
    patrimonio = bilancio.get("patrimonio_netto", 1) or 1
    debiti = bilancio.get("debiti", 0) or 0

    # Variabili di calcolo
    fondo_perduto = 0
    credito_imposta = 0
    finanziamento = 0
    aliquota = 0.27
    ratio = 0
    rata = 0
    cashflow_post = 0
    incremento_fatturato = investimento * 0.2
    incremento_ebitda = incremento_fatturato * 0.3
    nuova_redditivita = ebitda + incremento_ebitda

    # Inizializza risultato
    risultato = {
        "bando": titolo,
        "tipo_agevolazione": tipo_agevolazione,
        "investimento": investimento
    }

    forma = tipo_agevolazione.lower()

    # Fondo perduto
    if "fondo perduto" in forma:
        fondo_perduto = investimento * 0.5
        risultato["agevolazione_ottenibile"] = round(fondo_perduto, 2)
        risultato["liquidità_migliorata"] = f"{fondo_perduto:,.0f} €"

    # Credito d'imposta
    if "credito imposta" in forma:
        credito_imposta = investimento * 0.4
        risparmio_fiscale = credito_imposta * aliquota
        risultato["agevolazione_ottenibile"] = round(credito_imposta, 2)
        risultato["risparmio_fiscale"] = f"{risparmio_fiscale:,.0f} €"

    # Finanziamento agevolato
    if "finanziamento" in forma:
        tasso = 0.01
        durata = 5
        finanziamento = investimento
        rata = (finanziamento * tasso * (1 + tasso)**durata) / (((1 + tasso)**durata) - 1)
        cashflow_post = ebitda - rata
        risultato["rata_annua"] = round(rata, 2)
        risultato["cashflow_post_intervento"] = f"{cashflow_post:,.0f} €"

    # Reddività potenziale
    risultato["redditività_potenziale"] = f"{nuova_redditivita:,.0f} €"

    # Copertura finanziaria
    copertura = utile + liquidita
    if copertura >= investimento:
        risultato["copertura"] = "autonoma"
    else:
        risultato["copertura"] = "richiede supporto"

    # Nuovo debt/equity
    debito_totale = debiti + finanziamento
    if patrimonio > 0:
        ratio = debito_totale / patrimonio
    risultato["debt_equity_post"] = round(ratio, 2)

    return risultato
