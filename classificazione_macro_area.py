
from config import MACROAREA_THRESHOLDS

def classify_company(financials):
    ratio = {
        "current_ratio": financials["current_assets"] / financials["current_liabilities"],
        "debt_to_equity": financials["total_debt"] / financials["equity"],
        "ebitda_margin": financials["ebitda"] / financials["revenue"],
        "net_income": financials["net_income"]
    }

    thresholds = MACROAREA_THRESHOLDS
    macro_area = []

    if (ratio["current_ratio"] < thresholds["crisi"]["current_ratio"] and
        ratio["debt_to_equity"] > thresholds["crisi"]["debt_to_equity"] and
        ratio["ebitda_margin"] < thresholds["crisi"]["ebitda_margin"] and
        ratio["net_income"] < 0):
        macro_area.append("Crisi o Risanamento Aziendale")

    if (ratio["ebitda_margin"] >= thresholds["crescita"]["ebitda_margin"] and
        ratio["net_income"] > 0 and
        thresholds["crescita"]["debt_to_equity_min"] <= ratio["debt_to_equity"] <= thresholds["crescita"]["debt_to_equity_max"]):
        macro_area.append("Crescita e Sviluppo")

    if (ratio["ebitda_margin"] > thresholds["espansione"]["ebitda_margin"]):
        macro_area.append("Espansione e Sostenibilità")

    return macro_area if macro_area else ["Non classificato"]
