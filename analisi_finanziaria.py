from typing import Dict, Any


def calcola_dimensione(dipendenti: int, ricavi: float, totale_attivo: float) -> str:
    categorie = [
        {"nome": "Micro", "max_dip": 10, "max_ricavi": 2_000_000, "max_attivo": 2_000_000},
        {"nome": "Piccola", "max_dip": 50, "max_ricavi": 10_000_000, "max_attivo": 10_000_000},
        {"nome": "Media", "max_dip": 250, "max_ricavi": 50_000_000, "max_attivo": 43_000_000},
        {"nome": "Grande", "max_dip": float('inf'), "max_ricavi": float('inf'), "max_attivo": float('inf')}
    ]
    for categoria in categorie:
        count = 0
        if dipendenti <= categoria["max_dip"]:
            count += 1
        if ricavi <= categoria["max_ricavi"]:
            count += 1
        if totale_attivo <= categoria["max_attivo"]:
            count += 1
        if count >= 2:
            return categoria["nome"]
    return "Non classificata"


def calcola_indici(dati: Dict[str, Any]) -> Dict[str, float]:
    try:
        indici = {
            "ROE": dati["utile_netto"] / dati["patrimonio_netto"] if dati["patrimonio_netto"] else 0,
            "ROI": dati["ebit"] / dati["totale_attivo"] if dati["totale_attivo"] else 0,
            "ROS": dati["ebit"] / dati["ricavi"] if dati["ricavi"] else 0,
            "EBITDA_margin": dati["ebitda"] / dati["ricavi"] if dati["ricavi"] else 0,
            "Current_Ratio": dati["attivo_corrente"] / dati["passivo_corrente"] if dati["passivo_corrente"] else 0,
            "Quick_Ratio": (dati["attivo_corrente"] - dati.get("rimanenze", 0)) / dati["passivo_corrente"] if dati["passivo_corrente"] else 0,
            "Debt_Equity": dati["debiti_totali"] / dati["patrimonio_netto"] if dati["patrimonio_netto"] else 0,
            "PFN_EBITDA": (dati["debiti_finanziari"] - dati.get("liquidita", 0)) / dati["ebitda"] if dati["ebitda"] else 0,
            "Interest_Coverage": dati["ebit"] / dati["oneri_finanziari"] if dati["oneri_finanziari"] else 0,
            "Oneri_Fin_su_Ricavi": dati["oneri_finanziari"] / dati["ricavi"] if dati["ricavi"] else 0,
            "Autofinanziamento": dati["utile_netto"] + dati["ammortamenti"],
            "Solidita_Patrimoniale": dati["patrimonio_netto"] / dati["totale_attivo"] if dati["totale_attivo"] else 0,
            "Incidenza_Investimenti": dati["immobilizzazioni"] / dati["totale_attivo"] if dati["totale_attivo"] else 0,
            "Crescita_Ricavi": (dati["ricavi"] - dati["ricavi_anno_prec"]) / dati["ricavi_anno_prec"] if dati["ricavi_anno_prec"] else 0,
            "Variazione_Immobilizzazioni": (dati["immobilizzazioni"] - dati.get("immobilizzazioni_prec", 0)) / dati.get("immobilizzazioni_prec", 1),
            "Z_Score": (
                0.717 * ((dati["attivo_corrente"] - dati["passivo_corrente"]) / dati["totale_attivo"]) +
                0.847 * (dati["ebit"] / dati["totale_attivo"]) +
                3.107 * (dati["utile_netto"] / dati["totale_attivo"]) +
                0.420 * (dati["patrimonio_netto"] / dati["debiti_totali"]) +
                0.998 * (dati["ricavi"] / dati["totale_attivo"])
            ) if dati["totale_attivo"] and dati["debiti_totali"] else 0
        }
            # Calcolo rating MCC (approssimazione interna eVoluto)
            mcc = 5
            if indici["EBITDA_margin"] > 0.15 and indici["ROE"] > 0.1 and 0.5 <= indici["Debt_Equity"] <= 2:
            mcc = 1
            elif indici["EBITDA_margin"] > 0.10 and indici["ROE"] > 0 and indici["Debt_Equity"] <= 3:
            mcc = 2
            elif indici["EBITDA_margin"] > 0.05 and indici["ROE"] >= 0:
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
    if indici["ROE"] < 0: crisi_score += 1

    if indici["Autofinanziamento"] > 0: sviluppo_score += 1
    if indici["Solidita_Patrimoniale"] > 0.25: sviluppo_score += 1
    if indici["Incidenza_Investimenti"] > 0.2: sviluppo_score += 1

    if indici["Crescita_Ricavi"] > 0.05: espansione_score += 1
    if indici["EBITDA_margin"] > 0.1: espansione_score += 1
    if indici["ROS"] > 0.05: espansione_score += 1
    if indici["Variazione_Immobilizzazioni"] > 0.05: espansione_score += 1

    punteggi = {
        "Crisi": crisi_score,
        "Sviluppo": sviluppo_score,
        "Espansione": espansione_score
    }

    priorita = ["Crisi", "Sviluppo", "Espansione"]
    max_val = max(punteggi.values())
    macro_area = next(area for area in priorita if punteggi[area] == max_val)

    return macro_area
