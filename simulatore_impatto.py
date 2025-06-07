def simula_beneficio(bando, bilancio):
    risultato = {
        "bando": bando.get("titolo"),
        "tipo_agevolazione": bando.get("forma_agevolazione"),
        "investimento": bando.get("spesa_ammessa"),
    }
    
    investimento = bando.get("spesa_ammessa", 0)
    fondo_perduto = 0
    credito_imposta = 0
    finanziamento = 0
    aliquota = 0.27  # ipotesi

    utile_attuale = bilancio.get("utile_netto", 0)
    liquidita_attuale = bilancio.get("liquidita", 0)
    fatturato_attuale = bilancio.get("fatturato", 0)
    ebitda = bilancio.get("ebitda", 0)
    patrimonio_netto = bilancio.get("patrimonio_netto", 1)
    debiti = bilancio.get("debiti", 0)

    # FONDO PERDUTO
    if "fondo perduto" in bando.get("forma_agevolazione", "").lower():
        fondo_perduto = investimento * 0.5  # ipotesi 50%
        risultato["agevolazione_ottenibile"] = fondo_perduto
        risultato["liquidita_migliorata"] = f"+{fondo_perduto:,.0f} €"
    
    # CREDITO D’IMPOSTA
    elif "credito imposta" in bando.get("forma_agevolazione", "").lower():
        credito_imposta = investimento * 0.4  # ipotesi 40%
        risparmio_fiscale = credito_imposta * aliquota
        risultato["agevolazione_ottenibile"] = credito_imposta
        risultato["risparmio_fiscale"] = f"{risparmio_fiscale:,.0f} €"

    # FINANZIAMENTO AGEVOLATO
    elif "finanziamento" in bando.get("forma_agevolazione", "").lower():
        tasso = 0.01
        durata = 5  # anni
        finanziamento = investimento
        rata = (finanziamento * (tasso * (1 + tasso)**durata)) / (((1 + tasso)**durata) - 1)
        cashflow_post = ebitda - rata
        risultato["rata_annua"] = round(rata, 2)
        risultato["cashflow_post_intervento"] = f"{cashflow_post:,.0f} €"

    # REDDITIVITÀ
    incremento_fatturato = investimento * 0.2  # ipotesi 20%
    incremento_costi = investimento * 0.05
    utile_post = utile_attuale + incremento_fatturato - incremento_costi
    risultato["utile_atteso_post"] = f"+{utile_post:,.0f} €"

    # ROI
    roi = (incremento_fatturato - incremento_costi) / investimento if investimento else 0
    risultato["ROI"] = f"{roi*100:.1f}%"

    # DEBT/EQUITY POST
    nuovo_debit = debiti + finanziamento
    risultato["nuovo_debt_equity"] = round(nuovo_debit / patrimonio_netto, 2)

    return risultato
