def motivazione_solidita(punteggio: float) -> str:
    if punteggio >= 9:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda presenta una solidità ECCELLENTE. "
            "Il bando selezionato è pienamente coerente con la situazione economico-finanziaria e favorisce imprese con performance di eccellenza. 🔵"
        )
    elif punteggio >= 7:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda mostra una solidità ALTA. "
            "Il bando è compatibile con la struttura economica e può supportare progetti di sviluppo e crescita. 🟢"
        )
    elif punteggio >= 5:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda presenta una solidità MEDIA. "
            "Il bando è coerente con le caratteristiche finanziarie attuali e offre opportunità di consolidamento. 🟡"
        )
    elif punteggio >= 3:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda ha una solidità BASSA. "
            "L'accesso al bando è possibile ma richiede un'attenta pianificazione delle risorse. 🟠"
        )
    else:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda si trova in una situazione CRITICA. "
            "L'accesso al bando è consentito, ma sarà necessaria una strategia di rafforzamento per garantire la sostenibilità del progetto. 🔴"
        )
