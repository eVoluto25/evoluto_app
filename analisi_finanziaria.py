from typing import Dict

def calcola_indici(dati: dict) -> dict:
    try:
        # Safe cast con fallback 0
        ricavi = float(dati.get("ricavi") or 0)
        utile_netto = float(dati.get("utile_netto") or 0)
        ammortamenti = float(dati.get("ammortamenti") or 0)
        ebitda = float(dati.get("ebitda") or 0)
        ebit = float(dati.get("ebit") or 0)
        liquidita = float(dati.get("liquidità") or 0)
        debiti_finanziari = float(dati.get("debiti_finanziari") or 0)
        debiti_totali = float(dati.get("debiti_totali") or 0)
        patrimonio_netto = float(dati.get("patrimonio_netto") or 0)
        attivo_corrente = float(dati.get("attivo_corrente") or 0)
        passivo_corrente = float(dati.get("passivo_corrente") or 0)
        totale_attivo = float(dati.get("totale_attivo") or 0)
        immobilizzazioni = float(dati.get("immobilizzazioni") or 0)
        immobilizzazioni_prec = float(dati.get("immobilizzazioni_prec") or 0)
        ricavi_anno_prec = float(dati.get("ricavi_anno_prec") or 0)
        oneri_finanziari = float(dati.get("oneri_finanziari") or 0)
        rimanenze = float(dati.get("rimanenze") or 0)

        indici = {
            "EBITDA_margin": ebitda / ricavi if ricavi else 0,
            "Current_Ratio": attivo_corrente / passivo_corrente if passivo_corrente else 0,
            "Quick_Ratio": (attivo_corrente - rimanenze) / passivo_corrente if passivo_corrente else 0,
            "Debt_Equity": debiti_totali / patrimonio_netto if patrimonio_netto else 0,
            "PFN_EBITDA": (debiti_finanziari - liquidita) / ebitda if ebitda else 0,
            "Interest_Coverage": ebit / oneri_finanziari if oneri_finanziari else 0,
            "Oneri_Fin_su_Ricavi": oneri_finanziari / ricavi if ricavi else 0,
            "Autofinanziamento": utile_netto + ammortamenti,
            "Solidità_Patrimoniale": patrimonio_netto / totale_attivo if totale_attivo else 0,
            "Incidenza_Investimenti": immobilizzazioni / totale_attivo if totale_attivo else 0,
            "Crescita_Ricavi": (ricavi - ricavi_anno_prec) / ricavi_anno_prec if ricavi_anno_prec else 0,
            "Variazione_Immobilizzazioni": (immobilizzazioni - immobilizzazioni_prec) / immobilizzazioni_prec if immobilizzazioni_prec else 0,
        }

        indici["Z_Score"] = (
            0.717 * ((attivo_corrente - passivo_corrente) / totale_attivo) +
            0.847 * (ebit / totale_attivo) +
            3.107 * (utile_netto / totale_attivo) +
            0.420 * (patrimonio_netto / debiti_totali if debiti_totali else 0) +
            0.998 * (ricavi / totale_attivo)
        ) if totale_attivo else 0

        # MCC rating
        mcc = 5
        if indici["EBITDA_margin"] > 0.15 and utile_netto > 0 and 0.5 <= indici["Debt_Equity"] <= 2:
            mcc = 1
        elif indici["EBITDA_margin"] > 0.10 and utile_netto > 0 and indici["Debt_Equity"] <= 3:
            mcc = 2
        elif indici["EBITDA_margin"] > 0.05 and utile_netto >= 0:
            mcc = 3
        elif indici["EBITDA_margin"] > 0:
            mcc = 4

        indici["MCC"] = mcc
        return indici

    except Exception as e:
        return {"errore": str(e)}

def assegna_macro_area(indici: Dict[str, float]) -> str:
    crisi_score = 0
    sviluppo_score = 0
    espansione_score = 0

    if indici["Current_Ratio"] < 1: crisi_score += 1
    if indici["Debt_Equity"] > 2: crisi_score += 1
    if indici["Interest_Coverage"] < 1: crisi_score += 1
    if indici["EBITDA_margin"] < 0.05: crisi_score += 1
    if indici["Autofinanziamento"] <= 0: crisi_score += 1

    if indici["Autofinanziamento"] > 0: sviluppo_score += 1
    if indici["Solidità_Patrimoniale"] > 0.2: sviluppo_score += 1
    if indici["Incidenza_Investimenti"] > 0.2: sviluppo_score += 1

    if indici["Crescita_Ricavi"] > 0.05: espansione_score += 1
    if indici["EBITDA_margin"] > 0.10: espansione_score += 1
    if indici["Z_Score"] > 1.8: espansione_score += 1

    scores = {
        "Crisi": crisi_score,
        "Sviluppo": sviluppo_score,
        "Espansione": espansione_score
    }

    return max(scores, key=scores.get)

def calcola_dimensione(dipendenti: int, ricavi: float, totale_attivo: float) -> str:
    soglie = [
        ("Micro", 10, 2_000_000, 2_000_000),
        ("Piccola", 50, 10_000_000, 10_000_000),
        ("Media", 250, 50_000_000, 43_000_000),
        ("Grande", float("inf"), float("inf"), float("inf")),
    ]

    for nome, max_dip, max_ric, max_att in soglie:
        criteri = 0
        if dipendenti <= max_dip: criteri += 1
        if ricavi <= max_ric: criteri += 1
        if totale_attivo <= max_att: criteri += 1
        if criteri >= 2:
            return nome

    return "Non Classificata"