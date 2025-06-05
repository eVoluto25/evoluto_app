
def assegna_macroarea(indici: dict) -> str:
    # 🔴 Crisi o Risanamento Aziendale
    crisi = False
    if indici.get("current_ratio", 1) < 1:
        crisi = True
    if indici.get("debt_equity_ratio", 0) > 2:
        crisi = True
    if indici.get("interest_coverage_ratio", 1) < 1:
        crisi = True
    if indici.get("ebitda_margin", 1) < 0.05:
        crisi = True
    if indici.get("utile_netto", 0) < 0:
        crisi = True
    if crisi:
        return "Crisi"

    # 🟠 Crescita e Sviluppo (Start up, PMI, investimenti)
    crescita = False
    autofinanziamento = indici.get("capacita_autofinanziamento", 0)
    patrimonio = indici.get("patrimonio_netto", 1)
    totale_attivo = indici.get("totale_attivo_bilancio", 1)
    immobilizzazioni = indici.get("immobilizzazioni_totali", 0)

    solidita_patrimoniale = patrimonio / totale_attivo if totale_attivo else 0
    incidenza_investimenti = immobilizzazioni / totale_attivo if totale_attivo else 0

    if autofinanziamento > 0:
        crescita = True
    if solidita_patrimoniale > 0.2:
        crescita = True
    if incidenza_investimenti > 0.2:
        crescita = True
    if indici.get("spese_ricerca_sviluppo", 0) > 0:
        crescita = True
    if crescita:
        return "Crescita"

    # 🟢 Espansione, Mercati Esteri e Transizione Ecologica
    # NB: Qui alcuni dati non sono sempre disponibili da XBRL, quindi usiamo proxy
    espansione = False
    if indici.get("ebitda", 0) > 0:
        espansione = True
    if indici.get("spese_ricerca_sviluppo", 0) > 0:
        espansione = True
    if incidenza_investimenti > 0.25:
        espansione = True
    if indici.get("costi_ambientali", 0) > 0:
        espansione = True
    if indici.get("ebitda_margin", 0) > 0.10:
        espansione = True
    if espansione:
        return "Espansione"

    return "Gestione"
