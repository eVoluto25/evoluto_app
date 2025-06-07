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
    liquidità_attuale = bilancio.get("liquidità", 0) or 0
    fatturato_attuale = bilancio.get("fatturato", 0) or 0
    ebitda = bilancio.get("ebitda", 0) or 0
    patrimonio_netto = bilancio.get("patrimonio_netto", 1) or 1
    debiti = bilancio.get("debiti", 0) or 0

    forma_agevolazione = bando.get("forma_agevolazione", "").lower()

    # Fondo perduto
    if "fondo perduto" in forma_agevolazione:
        fondo_perduto = investimento * 0.5
        risultato["agevolazione_ottenibile"] = round(fondo_perduto, 2)
        risultato["liquidità_migliorata"] = f"{fondo_perduto:,.0f} €"

    # Credito d’imposta
    elif "credito imposta" in forma_agevolazione:
        credito_imposta = investimento * 0.4
        risparmio_fiscale = credito_imposta * aliquota
        risultato["agevolazione_ottenibile"] = round(credito_imposta, 2)
        risultato["risparmio_fiscale"] = f"{risparmio_fiscale:,.0f} €"

    # Finanziamento agevolato
    elif "finanziamento" in forma_agevolazione:
        tasso = 0.01
        durata = 5
        finanziamento = investimento
        rata = (finanziamento * (tasso * (1 + tasso)**durata)) / (((1 + tasso)**durata) - 1)
        cashflow_post = ebitda - rata
        risultato["rata_annua"] = round(rata, 2)
        risultato["cashflow_post_intervento"] = f"{cashflow_post:,.0f} €"

    # Redditività
    incremento_fatturato = investimento * 0.2
    incremento_ebitda = incremento_fatturato * 0.3
    nuova_redditività = ebitda + incremento_ebitda
    risultato["redditività_potenziale"] = f"{nuova_redditività:,.0f} €"

    # Copertura finanziaria
    autofinanziamento = liquidità_attuale + utile_attuale
    sostenibilità = autofinanziamento >= investimento
    risultato["copertura"] = "autonoma" if sostenibilità else "richiede supporto"

    # Debt/Equity post intervento
    debito_totale = debiti + finanziamento
    nuovo_ratio = debito_totale / patrimonio_netto if patrimonio_netto else 0
    risultato["debt_equity_post"] = round(nuovo_ratio, 2)

    return risultato
