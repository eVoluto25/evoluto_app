
def classifica_macro_area(indici):
    """
    Assegna una macro-area aziendale in base agli indici finanziari forniti.
    Gli indici devono essere passati come dizionario con i seguenti campi:
    - current_ratio
    - debt_equity
    - interest_coverage
    - ebitda_margin
    - utile_netto
    - autofinanziamento
    - solidita_patrimoniale
    - incidenza_investimenti
    - r_and_d
    - crescita_fatturato
    - ros
    - variazione_immobilizzazioni
    """

    punteggi = {"1": 0, "2": 0, "3": 0}

    # Macroarea 1 - Crisi o Risanamento
    if indici.get("current_ratio", 2) < 1.1:
        punteggi["1"] += 1
    if indici.get("debt_equity", 0) > 2.2:
        punteggi["1"] += 1
    if indici.get("interest_coverage", 2) < 1:
        punteggi["1"] += 1
    if indici.get("ebitda_margin", 10) < 5:
        punteggi["1"] += 1
    if indici.get("utile_netto", 1) < 0:
        punteggi["1"] += 1

    # Macroarea 2 - Crescita e Sviluppo
    if indici.get("autofinanziamento", 0) > 0:
        punteggi["2"] += 1
    if indici.get("solidita_patrimoniale", 0.1) > 0.2:
        punteggi["2"] += 1
    if indici.get("incidenza_investimenti", 0) > 0.1:
        punteggi["2"] += 1
    if indici.get("r_and_d", False):
        punteggi["2"] += 1

    # Macroarea 3 - Espansione, Mercati Esteri, Transizione
    if indici.get("crescita_fatturato", 0) > 0.05:
        punteggi["3"] += 1
    if indici.get("ebitda_margin", 0) > 10:
        punteggi["3"] += 1
    if indici.get("ros", 0) > 5:
        punteggi["3"] += 1
    if indici.get("variazione_immobilizzazioni", 0) > 0:
        punteggi["3"] += 1

    return max(punteggi, key=punteggi.get)
