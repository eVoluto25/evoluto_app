
def macroarea_match(obiettivo_finalita, macroarea):
    obiettivo_finalita = obiettivo_finalita.lower()

    crisi_keywords = ["crisi", "liquidità", "inclusione sociale"]
    crescita_keywords = ["start up", "sviluppo", "investimenti", "giovanile", "femminile"]
    espansione_keywords = ["internazionalizzazione", "transizione ecologica", "innovazione", "ricerca"]

    if macroarea == "crisi":
        return any(kw in obiettivo_finalita for kw in crisi_keywords)
    elif macroarea == "crescita":
        return any(kw in obiettivo_finalita for kw in crescita_keywords)
    elif macroarea == "espansione":
        return any(kw in obiettivo_finalita for kw in espansione_keywords)
    return False


def calcola_punteggio_bando(bando, azienda, indici):
    punteggio = 0

    # A - Compatibilità con la Macro Area (30%)
    if macroarea_match(bando["Obiettivo_Finalita"], azienda["macroarea"]):
        punteggio += 30
    else:
        punteggio += 10  # punteggio minimo se non perfettamente allineato

    # B - Solidità Finanziaria (25%)
    solidita = 0
    if indici["ebitda_margin"] > 0.10:
        solidita += 10
    if indici["utile_netto"] > 0:
        solidita += 10
    if 0.5 <= indici["debt_equity"] <= 2:
        solidita += 5
    punteggio += solidita

    # C - Forma dell’agevolazione (15%)
    forma = bando.get("Forma_Agevolazione", "").lower()
    if "fondo perduto" in forma:
        punteggio += 15
    elif "credito d'imposta" in forma:
        punteggio += 10
    elif "finanziamento" in forma:
        punteggio += 5

    return punteggio
