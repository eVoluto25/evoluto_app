
import math

def calcola_score_bando(bando: dict, azienda: dict) -> dict:
    score = 0
    log = []

    # A. Macroarea (30 pt)
    if azienda['macroarea'] in bando['Obiettivo_Finalita']:
        score += 30
        log.append("Match perfetto macroarea +30")
    elif azienda['macroarea_alternativa'] in bando['Obiettivo_Finalita']:
        score += 20
        log.append("Match secondaria macroarea +20")
    else:
        log.append("Nessuna corrispondenza macroarea")

    # B. Solidità finanziaria (25 pt)
    indici = azienda.get("indici", {})
    if indici.get("EBITDA Margin", 0) > 10:
        score += 10
    else:
        score -= 5
    if indici.get("Utile Netto", 0) > 0:
        score += 10
    else:
        score -= 5
    if 0.5 <= indici.get("Debt/Equity", 0) <= 2:
        score += 5
    else:
        score -= 3

    # C. Forma agevolazione (15 pt)
    forma = bando.get("Forma_agevolazione", "").lower()
    if "fondo" in forma:
        score += 15
    elif "credito" in forma:
        score += 12
    elif "finanziamento" in forma:
        score += 10
    else:
        score += 0

    # D. Dimensioni azienda (10 pt)
    if azienda['dimensione'] == bando.get("Dimensioni", ""):
        score += 10
    elif azienda['dimensione'] in bando.get("Dimensioni", ""):
        score += 6

    # E. Cofinanziamento (10 pt)
    if indici.get("Quick Ratio", 0) > 1:
        score += 5
    if indici.get("PFN/PN", math.inf) < 1:
        score += 3
    if indici.get("Cash Flow Operativo", 0) > 0:
        score += 2
    if score < 3:
        score -= 5

    # F. Settore/Territorio (10 pt)
    if azienda['codice_ateco'] in bando.get("Codici_ATECO", "") and azienda['regione'] in bando.get("Regioni", ""):
        score += 10
    elif azienda['codice_ateco'] in bando.get("Codici_ATECO", "") or azienda['regione'] in bando.get("Regioni", ""):
        score += 5

    fascia = "Alta probabilità ✅" if score >= 80 else "Media ⚠️" if score >= 60 else "Bassa ❌" if score >= 40 else "ND → Claude"

    return {
        "id": bando["ID_Incentivo"],
        "titolo": bando["Titolo"],
        "score": score,
        "fascia": fascia,
        "log": log
    }
