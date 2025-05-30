
def filtra_bandi_per_macroarea(bandi, macroarea):
    categorie_rilevanti = {
        "🔴 1. Crisi o Risanamento Aziendale": [
            "Crisi d’impresa", "Sostegno liquidità", "Inclusione sociale"
        ],
        "🟠 2. Crescita e Sviluppo (Start up, PMI, investimenti)": [
            "Start up", "Sviluppo d’impresa", "Investimenti", "Imprenditoria giovanile", "Imprenditoria femminile"
        ],
        "🟢 3. Espansione, Mercati Esteri e Transizione Ecologica": [
            "Internazionalizzazione", "Ricerca", "Transizione ecologica", "Innovazione"
        ]
    }

    rilevanti = categorie_rilevanti.get(macroarea, [])
    bandi_filtrati = [
        bando for bando in bandi
        if any(cat.lower() in bando.get("categoria", "").lower() for cat in rilevanti)
    ]
    return bandi_filtrati
