# scoring_bandi.py – scoring 100 pt + fallback Claude

import logging
import json
import os

# Lettura pesi dinamici se presenti
def carica_pesi():
    try:
        with open("scoring_pesi.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "macroarea": 30,
            "finanziaria": 25,
            "forma": 15,
            "dimensione": 10,
            "cofinanziamento": 10,
            "settore_territorio": 10
        }

def calcola_scoring_bando(bando: dict, azienda: dict, indici: dict, macroarea: str) -> dict:
    pesi = carica_pesi()
    score = 0
    dettaglio = {}
    note = []
    forward_to_claude = False

    # A. Macroarea (30 pt)
    obiettivo = (bando.get("Obiettivo_Finalita") or "").lower()
    if macroarea.lower() in obiettivo:
        punteggio = pesi["macroarea"]
    elif any(kw in obiettivo for kw in ["sviluppo", "ricerca", "impresa"]):
        punteggio = 20
    elif not obiettivo:
        punteggio = 0
        forward_to_claude = True
        note.append("Obiettivo_Finalita non definito")
    else:
        punteggio = 0
    score += punteggio
    dettaglio["macroarea"] = punteggio

    # B. Solidità Finanziaria (25 pt)
    pf = 0
    if indici.get("calcola_ebitda_margin", 0) > 0.10: pf += 10
    elif indici.get("calcola_ebitda_margin") is None: pf -= 3

    if azienda.get("utile_netto", 0) > 0: pf += 10
    elif azienda.get("utile_netto") is None: pf -= 3
    elif azienda.get("utile_netto") < 0: pf -= 5

    d_e = indici.get("calcola_indebitamento")
    if d_e is not None:
        if 0.5 <= d_e <= 2: pf += 5
        else: pf -= 5
    else:
        pf -= 3

    pf = max(0, pf)
    score += pf
    dettaglio["finanziaria"] = pf

    # C. Forma agevolazione (15 pt)
    forma = (bando.get("Forma_agevolazione") or "").lower()
    if "fondo" in forma: p = 15
    elif "credito" in forma: p = 12
    elif "finanziamento" in forma: p = 10
    else: p = 0
    score += p
    dettaglio["forma"] = p

    # D. Dimensione azienda (10 pt)
    azi_dim = azienda.get("dimensione", "").lower()
    bando_dim = (bando.get("Dimensioni") or "").lower()
    if azi_dim and azi_dim in bando_dim: p = 10
    elif azi_dim and any(x in bando_dim for x in ["micro", "pmi", "media"]) and azi_dim != bando_dim: p = 6
    elif not azi_dim: p = 0; note.append("Dimensione azienda mancante")
    else: p = 0
    score += p
    dettaglio["dimensione"] = p

    # E. Cofinanziamento (10 pt)
    pc = 0
    if indici.get("calcola_quick_ratio", 0) > 1: pc += 5
    if indici.get("calcola_pfn_su_patrimonio", 0) < 1: pc += 3
    if azienda.get("cash_flow_operativo", 0) > 0: pc += 2
    if pc == 0: note.append("Cofinanziamento debole o assente")
    score += pc
    dettaglio["cofinanziamento"] = pc

    # F. Settore e territorio (10 pt)
    pt = 0
    ateco_az = azienda.get("ateco", "")
    reg_az = azienda.get("regione", "")
    codici_bando = (bando.get("Codici_ATECO") or "").lower()
    regioni_bando = (bando.get("Regioni") or "").lower()

    if ateco_az.lower() in codici_bando and reg_az.lower() in regioni_bando:
        pt = 10
    elif ateco_az.lower() in codici_bando or reg_az.lower() in regioni_bando:
        pt = 5
    else:
        pt = 0
        if not ateco_az: note.append("Codice ATECO azienda mancante")
    score += pt
    dettaglio["settore_territorio"] = pt

    # Fascia
    if score >= 80: fascia = "Alta probabilità"
    elif score >= 60: fascia = "Media probabilità"
    elif score >= 40: fascia = "Bassa probabilità"
    else:
        fascia = "Non idoneo"
        forward_to_claude = True

    return {
        "score": round(score, 2),
        "fascia": fascia,
        "dettaglio": dettaglio,
        "note": note,
        "forward_to_claude": forward_to_claude
    }