def assegna_macro_area(z_score: float, mcc_rating: float) -> str:
    if z_score >= 2.5 and mcc_rating <= 3:
        print("# Macro area assegnata: Espansione (z ≥ 2.5 e MCC ≤ 3)")
        return "Espansione"
    elif 1.8 <= z_score < 2.5 and 4 <= mcc_rating <= 6:
        print("# Macro area assegnata: Sviluppo (1.8 ≤ z < 2.5 e 4 ≤ MCC ≤ 6)")
        return "Sviluppo"
    else:
        print("# Macro area assegnata: Crisi (z < 1.8 o MCC ≥ 7)")
        return "Crisi"
