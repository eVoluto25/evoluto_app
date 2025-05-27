
def calcola_grado_compatibilità(bando, azienda):
    motivazioni = []
    criticità = []
    punteggio = 0

    # Matching dimensione
    dimensioni_ok = bando.get("dimensione_impresa", [])  # es: ["PMI", "Micro"]
    if azienda.get("dimensione") in dimensioni_ok:
        motivazioni.append("✔ Dimensione azienda compatibile")
        punteggio += 2
    else:
        criticità.append("✖ Dimensione azienda non compatibile")

    # Matching settore (ATECO)
    ateco_azienda = azienda.get("settori_ateco", [])
    ateco_bando = bando.get("ateco_ammessi", [])
    if any(cod in ateco_bando for cod in ateco_azienda):
        motivazioni.append("✔ Settore (ATECO) ammesso")
        punteggio += 2
    else:
        criticità.append("✖ Codice ATECO non previsto")

    # Matching geografico
    localita_ok = bando.get("localita", "")
    if localita_ok in azienda.get("localita", ""):
        motivazioni.append("✔ Area geografica compatibile")
        punteggio += 1
    else:
        criticità.append("✖ Area geografica non compatibile")

    # Matching finalità
    finalita = azienda.get("finalita", [])
    finalita_bando = bando.get("finalita", [])
    if any(f in finalita_bando for f in finalita):
        motivazioni.append("✔ Finalità coerente con il bando")
        punteggio += 2
    else:
        criticità.append("✖ Finalità non allineata")

    # Matching forma agevolazione
    forma_ok = bando.get("forma_agevolazione", "")
    if forma_ok in azienda.get("forme_sostenibili", []):
        motivazioni.append("✔ Forma dell’agevolazione sostenibile")
        punteggio += 1
    else:
        criticità.append("✖ Forma agevolazione potenzialmente critica")

    if punteggio >= 7:
        compatibilità = "Alta"
    elif punteggio >= 4:
        compatibilità = "Media"
    else:
        compatibilità = "Bassa"

    return compatibilità, motivazioni, criticità, punteggio


def match_bandi_per_compatibilita_e_priorita(azienda_data, bandi_list):
    risultati = []

    for bando in bandi_list:
        compatibilità, motivazioni, criticità, score = calcola_grado_compatibilità(bando, azienda_data)
        bando["compatibilità"] = compatibilità
        bando["motivazione"] = motivazioni
        bando["criticità"] = criticità
        bando["score"] = score
        risultati.append(bando)

    risultati.sort(key=lambda b: -b["score"])
    top_10_bandi = risultati[:10]
    extra_10_bandi = risultati[10:20]

    return top_10_bandi, extra_10_bandi
