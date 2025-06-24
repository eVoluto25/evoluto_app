def assegna_macro_area(z_score: float, mcc_rating: float) -> str:
    if z_score >= 2.5 and mcc_rating >= 7:
        print("# Macro area assegnata: Espansione (z ≥ 2.5 e MCC ≥ 7)")
        return "Espansione"
    elif z_score < 1.0 and mcc_rating < 4:
        print("# Macro area assegnata: Crisi (z < 1.0 e MCC < 4)")
        return "Crisi"
    elif z_score < 1.0 and mcc_rating >= 7:
        print("# Macro area assegnata: Sviluppo (z critico ma MCC solido)")
        return "Sviluppo"
    elif z_score >= 2.5 and mcc_rating < 4:
        print("# Macro area assegnata: Sviluppo (MCC critico ma Z-score solido)")
        return "Sviluppo"
    elif 1.0 <= z_score < 2.5 and 4 <= mcc_rating < 7:
        print("# Macro area assegnata: Sviluppo (zona intermedia)")
        return "Sviluppo"
    else:
        print("# Macro area assegnata: Sviluppo (default intermedio)")
        return "Sviluppo"
