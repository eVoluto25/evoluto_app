# matching_bandi.py

import re

def normalizza_ateco(codice):
    if not codice:
        return None
    return re.sub(r"[^\d]", "", codice)[:2]  # Es: "68.10.00" → "68"

def normalizza_regione(regione):
    regione = regione.lower().strip()
    mapping = {
        "lombardia": "nord", "piemonte": "nord", "veneto": "nord",
        "lazio": "centro", "toscana": "centro", "marche": "centro",
        "campania": "sud", "sicilia": "sud", "calabria": "sud",
        "nazionale": "tutte"
    }
    return mapping.get(regione, regione)

def match_bando(azienda, bando):
    match_ateco = False
    match_regione = False
    fallback = False
    log = []

    ateco_azienda = normalizza_ateco(azienda.get("codice_ateco"))
    ateco_bando = [normalizza_ateco(c) for c in bando.get("Codici_ATECO", [])]

    if "tutti" in bando.get("Codici_ATECO", []) or ateco_azienda in ateco_bando:
        match_ateco = True
    else:
        log.append("Codice ATECO non compatibile")
        fallback = True

    regione_azienda = normalizza_regione(azienda.get("regione"))
    regioni_bando = [normalizza_regione(r) for r in bando.get("Regioni", [])]

    if "nazionale" in bando.get("Regioni", []) or regione_azienda in regioni_bando:
        match_regione = True
    else:
        log.append("Regione non compatibile")
        fallback = True

    obiettivo = bando.get("Obiettivo_Finalita", "").lower()
    if any(k in obiettivo for k in ["crisi", "liquidità", "inclusione"]):
        obiettivo_macroarea = "CRISI"
    elif any(k in obiettivo for k in ["start", "sviluppo", "investimenti", "giovanile", "femminile"]):
        obiettivo_macroarea = "CRESCITA"
    elif any(k in obiettivo for k in ["internaz", "ricerca", "innovazione", "ecologica"]):
        obiettivo_macroarea = "ESPANSIONE"
    else:
        obiettivo_macroarea = None
        log.append("Obiettivo_Finalita ambiguo")
        fallback = True

    return {
        "match_ateco": match_ateco,
        "match_regione": match_regione,
        "obiettivo_macroarea": obiettivo_macroarea,
        "fallback": fallback,
        "log_matching": log
    }
