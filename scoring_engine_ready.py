import logging

logging.basicConfig(level=logging.INFO)

def calcola_punteggio_bando(bando, azienda, indici):
    punteggio = 0
    log = {}

    # A. Macroarea (30%)
    if bando.get("Macroarea") == azienda.get("Macroarea"):
        punteggio += 30
        log["Macroarea"] = 30
    elif bando.get("Macroarea") in azienda.get("Macroarea_Compatibili", []):
        punteggio += 15
        log["Macroarea"] = 15
    else:
        log["Macroarea"] = 0

    # B. Solidità Finanziaria (25%)
    solidita = 0
    if indici.get("EBITDA_margin", 0) > 0.10:
        solidita += 10
    if indici.get("Utile_Netto", 0) > 0:
        solidita += 10
    if 0.5 <= indici.get("Debt_Equity", 2.1) <= 2:
        solidita += 5
    log["Solidità_Finanziaria"] = solidita
    punteggio += solidita

    # C. Forma agevolazione (15%)
    forma = bando.get("Forma_Agevolazione", "").lower()
    if "fondo perduto" in forma:
        punteggio += 15
        log["Agevolazione"] = 15
    elif "credito d’imposta" in forma or "credito di imposta" in forma:
        punteggio += 10
        log["Agevolazione"] = 10
    elif "finanziamento" in forma:
        punteggio += 5
        log["Agevolazione"] = 5
    else:
        log["Agevolazione"] = 0

    # D. Dimensione Aziendale (10%)
    if azienda.get("Dimensione") and azienda["Dimensione"].lower() in bando.get("Dimensioni", "").lower():
        punteggio += 10
        log["Dimensione"] = 10
    else:
        log["Dimensione"] = 0

    # E. Co-finanziamento (10%)
    if azienda.get("Capacita_CoFinanziamento", False):
        punteggio += 10
        log["CoFinanziamento"] = 10
    else:
        log["CoFinanziamento"] = 0

    # F. Territorio e ATECO (10%)
    terr = 0
    if azienda.get("Regione") and azienda["Regione"] in bando.get("Regioni", ""):
        terr += 5
    if azienda.get("Codice_ATECO") and azienda["Codice_ATECO"] in bando.get("Codici_ATECO", ""):
        terr += 5
    log["Territorio_ATECO"] = terr
    punteggio += terr

    # Classificazione qualitativa
    if punteggio >= 80:
        livello = "Alta probabilità ✅"
    elif punteggio >= 50:
        livello = "Media probabilità ⚠️"
    else:
        livello = "Bassa probabilità ❌"

    return {
        "punteggio": punteggio,
        "livello": livello,
        "dettaglio": log
    }
