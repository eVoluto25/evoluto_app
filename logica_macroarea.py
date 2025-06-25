def assegna_macro_area(z_score: float, mcc_rating: float, utile_netto: float, ebitda_margin: float) -> str:
    # Normalizzazione punteggi (0–100)
    punteggio = 0

    # Z-score (peso 30%)
    if z_score >= 3:
        punteggio += 30
    elif z_score >= 2:
        punteggio += 22
    elif z_score >= 1:
        punteggio += 15
    else:
        punteggio += 5

    # MCC (peso 30%)
    if mcc_rating >= 8:
        punteggio += 30
    elif mcc_rating >= 6:
        punteggio += 20
    elif mcc_rating >= 4:
        punteggio += 12
    else:
        punteggio += 5

    # Utile netto (peso 20%)
    if utile_netto > 0:
        punteggio += 20
    else:
        punteggio += 5

    # EBITDA margin (peso 20%)
    if ebitda_margin >= 15:
        punteggio += 20
    elif ebitda_margin >= 10:
        punteggio += 15
    elif ebitda_margin > 0:
        punteggio += 8
    else:
        punteggio += 2

    print(f"# Punteggio totale: {punteggio}")

    if punteggio < 50:
        print("# Macro area assegnata: Sostegno")
        return "Sostegno"
    else:
        print("# Macro area assegnata: Innovazione")
        return "Innovazione"
