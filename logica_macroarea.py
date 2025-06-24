def assegna_macro_area(z_score: float, mcc_rating: float) -> str:
    if z_score >= 2.5 and mcc_rating <= 3:
        print("# Macro area assegnata: Espansione (z ≥ 2.5 e MCC ≤ 3)")
        return "Espansione"
    elif 1.0 <= z_score < 2.5 and 4 <= mcc_rating <= 6:
        print("# Macro area assegnata: Sviluppo (1.0 ≤ z < 2.5 e 4 ≤ MCC ≤ 6)")
        return "Sviluppo"
    elif z_score < 1.0 and mcc_rating < 4:
        print("# Macro area assegnata: Crisi (z < 1.0 e MCC < 4)")
        return "Crisi"
    else:
        print("# Macro area assegnata: Sviluppo (default intermedio)")
        return "Sviluppo"
