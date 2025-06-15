
# scoring_claude.py

def calcola_punteggio_bando(bando, azienda):
    punteggio = 0
    log = {}

    # 1. Solidità finanziaria (50%)
    solidita = 0
    ebitda = azienda.get("ebitda", 0)
    utile_netto = azienda.get("utile_netto", 0)
    debiti_finanziari = azienda.get("debiti_finanziari", 0)
    patrimonio_netto = azienda.get("patrimonio_netto", 0)
    z_score = azienda.get("z_score", None)
    mcc_rating = azienda.get("mcc_rating", None)

    # EBITDA positivo
    if ebitda > 0:
        solidita += 1
        log["ebitda_positivo"] = 1
    else:
        log["ebitda_positivo"] = 0

    # Utile positivo
    if utile_netto > 0:
        solidita += 1
        log["utile_positivo"] = 1
    else:
        log["utile_positivo"] = 0

    # Debt/Equity
    debt_equity = debiti_finanziari / patrimonio_netto if patrimonio_netto else None
    if debt_equity is not None and 0.5 <= debt_equity <= 2:
        solidita += 1
        log["debt_equity_ok"] = 1
    else:
        log["debt_equity_ok"] = 0

    # Z-score critico
    if z_score is not None and z_score < 1.8:
        solidita -= 1
        log["z_score_critico"] = -1
    else:
        log["z_score_critico"] = 0

    # MCC critico
    if mcc_rating is not None and mcc_rating >= 4:
        solidita -= 1
        log["mcc_critico"] = -1
    else:
        log["mcc_critico"] = 0

    punteggio += max(0, solidita) * 50 / 5

    # 2. Forma dell’agevolazione (25%)
    forma = bando.get("forma_agevolazione", "").lower()
    if "fondo perduto" in forma:
        punteggio += 25
        log["forma_agevolazione"] = "fondo perduto"
    elif "credito d’imposta" in forma:
        punteggio += 12.5
        log["forma_agevolazione"] = "credito d’imposta"
    elif "finanziamento" in forma:
        punteggio += 6.25
        log["forma_agevolazione"] = "finanziamento"
    else:
        log["forma_agevolazione"] = "non specificata"

    # 3. Capacità di co-finanziamento (15%)
    if utile_netto > 0 and mcc_rating is not None and mcc_rating <= 3:
        punteggio += 15
        log["capacita_cofinanziamento"] = "alta"
    elif utile_netto < 0 and mcc_rating is not None and mcc_rating >= 4:
        punteggio -= 5
        log["capacita_cofinanziamento"] = "bassa"
    else:
        log["capacita_cofinanziamento"] = "media"

    # 4. Coerenza economica bando/azienda (10%)
    spesa_minima = bando.get("spesa_minima", None)
    totale_attivo = azienda.get("totale_attivo", None)
    if spesa_minima is not None and totale_attivo is not None:
        if spesa_minima <= 0.5 * totale_attivo:
            punteggio += 10
            log["coerenza_spesa"] = "coerente"
        else:
            log["coerenza_spesa"] = "non coerente"
    else:
        log["coerenza_spesa"] = "dati insufficienti"

    return round(punteggio, 2), log
