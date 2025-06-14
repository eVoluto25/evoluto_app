from typing import Dict

def calcola_indici(dati: dict) -> dict:
    try:
        indici = {
            "EBITDA_margin": dati["ebitda"] / dati["ricavi"] if dati["ricavi"] else 0,
            "Current_Ratio": dati["attivo_corrente"] / dati["passivo_corrente"] if dati["passivo_corrente"] else 0,
            "Quick_Ratio": (dati.get("attivo_corrente", 0) - dati.get("rimanenze", 0)) / dati["passivo_corrente"] if dati["passivo_corrente"] else 0,
            "Debt_Equity": dati["debiti_totali"] / dati["patrimonio_netto"] if dati["patrimonio_netto"] else 0,
            "PFN_EBITDA": (float(dati.get("debiti_finanziari") or 0) - float(dati.get("liquidità") or 0)) / dati["ebitda"] if dati["ebitda"] else 0,
            "Interest_Coverage": dati["ebit"] / dati["oneri_finanziari"] if dati["oneri_finanziari"] else 0,
            "Oneri_Fin_su_Ricavi": dati["oneri_finanziari"] / dati["ricavi"] if dati["ricavi"] else 0,
            "Autofinanziamento": dati["utile_netto"] + dati["ammortamenti"],
            "Solidità_Patrimoniale": dati["patrimonio_netto"] / dati["totale_attivo"] if dati["totale_attivo"] else 0,
            "Incidenza_Investimenti": dati["immobilizzazioni"] / dati["totale_attivo"] if dati["totale_attivo"] else 0,
            "Crescita_Ricavi": (dati["ricavi"] - dati["ricavi_anno_prec"]) / dati["ricavi_anno_prec"] if dati["ricavi_anno_prec"] else 0,
            "Variazione_Immobilizzazioni": (dati["immobilizzazioni"] - dati.get("immobilizzazioni_prec", 0)) / dati.get("immobilizzazioni_prec", 1)
        }

        indici["Z_Score"] = (
            0.717 * ((dati["attivo_corrente"] - dati["passivo_corrente"]) / dati["totale_attivo"]) +
            0.847 * (dati["ebit"] / dati["totale_attivo"]) +
            3.107 * (dati["utile_netto"] / dati["totale_attivo"]) +
            0.420 * (dati["patrimonio_netto"] / dati["debiti_totali"]) +
            0.998 * (dati["ricavi"] / dati["totale_attivo"])
        ) if dati["totale_attivo"] and dati["debiti_totali"] else 0

        # Calcolo rating MCC
        mcc = 5
        if indici["EBITDA_margin"] > 0.15 and dati["utile_netto"] > 0 and 0.5 <= indici["Debt_Equity"] <= 2:
            mcc = 1
        elif indici["EBITDA_margin"] > 0.10 and dati["utile_netto"] > 0 and indici["Debt_Equity"] <= 3:
            mcc = 2
        elif indici["EBITDA_margin"] > 0.05 and dati["utile_netto"] >= 0:
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
