# scoring_bandi.py

def calcola_score(bando, azienda):
    log = []
    score = 0
    fallback = False
    nd_counter = 0

    macroarea_bando = bando.get("obiettivo_macroarea")
    macroarea_azienda = azienda.get("macroarea_primaria")

    # A. Macroarea (30 pt)
    if macroarea_bando and macroarea_azienda:
        if macroarea_bando == macroarea_azienda:
            score += 30
        elif azienda.get("macroarea_alternativa") == macroarea_bando:
            score += 20
        else:
            log.append("Macroarea non coerente")
    else:
        fallback = True
        nd_counter += 1
        log.append("Macroarea non disponibile")

    # B. Solidità Finanziaria (25 pt)
    indici = azienda.get("indici", {})
    ebitda_margin = indici.get("calcola_ebitda_margin")
    utile_netto = azienda.get("utile_netto")
    debt_equity = indici.get("calcola_debt_equity")

    if ebitda_margin is not None and ebitda_margin > 0.10:
        score += 10
    elif ebitda_margin is None:
        nd_counter += 1
        log.append("EBITDA Margin ND")

    if utile_netto is not None and utile_netto > 0:
        score += 10
    elif utile_netto is None:
        nd_counter += 1
        log.append("Utile netto ND")

    if debt_equity is not None and 0.5 <= debt_equity <= 2:
        score += 5
    elif debt_equity is None:
        nd_counter += 1
        log.append("Debt/Equity ND")

    # C. Forma Agevolazione (15 pt)
    forma = bando.get("Forma_agevolazione", "").lower()
    if "fondo perduto" in forma:
        score += 15
    elif "credito" in forma:
        score += 12
    elif "finanziamento" in forma:
        score += 8
    else:
        nd_counter += 1
        log.append("Forma agevolazione non riconosciuta")

    # D. Dimensione (10 pt)
    dim_bando = bando.get("Dimensioni")
    dim_azienda = azienda.get("dimensione_impresa")
    if dim_bando == dim_azienda:
        score += 10
    elif dim_bando and dim_azienda:
        score += 6  # vicinanza
    else:
        nd_counter += 1
        log.append("Dimensione non definita")

    # E. Cofinanziamento (10 pt)
    quick = indici.get("calcola_quick_ratio")
    pfn_pn = indici.get("calcola_pfn_pn")
    cf = azienda.get("cash_flow_operativo")

    if quick and quick > 1:
        score += 5
    if pfn_pn and pfn_pn < 1:
        score += 3
    if cf and cf > 0:
        score += 2

    if all(x in (None, 0) for x in [quick, pfn_pn, cf]):
        score -= 5
        log.append("Cofinanziamento assente")
        nd_counter += 1

    # F. ATECO + Territorio (10 pt)
    if azienda.get("match_ateco") and azienda.get("match_regione"):
        score += 10
    elif azienda.get("match_ateco") or azienda.get("match_regione"):
        score += 5
    else:
        log.append("ATECO o regione non compatibili")
        nd_counter += 1

    # Diagnostica e trigger fallback
    if score < 40 or nd_counter >= 3 or azienda.get("dati_incompleti"):
        fallback = True

    return {
        "score": max(score, 0),
        "log_scoring": log,
        "forward_to_claude": fallback
    }
