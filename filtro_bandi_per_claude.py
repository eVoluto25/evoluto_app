# filtro_bandi_per_claude.py

def filtra_bandi_da_inviare_a_claude(bandi_scoring: list) -> list:
    """
    Restituisce solo i bandi da analizzare con Claude:
    - score tra 70 e 79
    - note ND o penalità
    - mismatch su ATECO o Regione
    - macroarea incerta
    - obiettivo finalità troppo breve
    """
    bandi_critici = []

    for voce in bandi_scoring:
        score = voce.get("Score", 0)
        scoring = voce.get("Scoring", {})
        bando = voce.get("Bando", {})
        macroarea = scoring.get("macroarea", "")

        critico = False

        if 70 <= score < 80:
            critico = True

        if "ND" in scoring.get("note", "") or "penalità" in scoring.get("note", ""):
            critico = True

        if macroarea in ["ND", "Multipla", "Ambigua"]:
            critico = True

        finalita = bando.get("Obiettivo_Finalita", "")
        if len(finalita.split()) < 10:
            critico = True

        # Controlli base su ATECO/Regione
        ateco_ok = scoring.get("match_ateco", True)
        regione_ok = scoring.get("match_regione", True)
        if not ateco_ok or not regione_ok:
            critico = True

        if critico:
            bandi_critici.append(voce)

    return bandi_critici