# matching_bandi.py

import re

def normalizza_ateco(codice):
    if not codice:
        return None
    return re.sub(r"[^\d]", "", codice)[:2]

def normalizza_regione(regione):
    if not regione:
        return None
    regione = regione.lower().strip()
    mapping = {
        "lombardia": "nord", "piemonte": "nord", "veneto": "nord",
        "liguria": "nord", "emilia-romagna": "nord",
        "toscana": "centro", "umbria": "centro", "marche": "centro", "lazio": "centro",
        "campania": "sud", "puglia": "sud", "calabria": "sud", "sicilia": "sud", "basilicata": "sud",
        "sardegna": "isole", "trentino": "nord", "friuli": "nord", "abruzzo": "centro"
    }
    return mapping.get(regione, regione)

def match_bando(azienda, bando):
    log = []
    fallback = False

    ateco_azienda = normalizza_ateco(azienda.get("codice_ateco"))
    ateco_bando = [normalizza_ateco(c) for c in bando.get("Codici_ATECO", [])]

    if "tutti" in bando.get("Codici_ATECO", []) or ateco_azienda in ateco_bando:
        match_ateco = True
    else:
        match_ateco = False
        log.append("Codice ATECO non compatibile")
        fallback = True

    regione_azienda = normalizza_regione(azienda.get("regione"))
    regioni_bando = [normalizza_regione(r) for r in bando.get("Regioni", [])]

    if "nazionale" in bando.get("Regioni", []) or regione_azienda in regioni_bando:
        match_regione = True
    else:
        match_regione = False
        log.append("Regione non compatibile")
        fallback = True

    obiettivo = bando.get("Obiettivo_Finalita", "").lower()
    if any(k in obiettivo for k in ["crisi", "liquidità", "inclusione"]):
        obiettivo_macroarea = "CRISI"
    elif any(k in obiettivo for k in ["start", "sviluppo", "investimenti", "giovanile", "femminile"]):
        obiettivo_macroarea = "CRESCITA"
    elif any(k in obiettivo for k in ["internaz", "ricerca", "innovazione", "ecologica", "green"]):
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