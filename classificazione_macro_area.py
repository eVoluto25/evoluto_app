
def classifica_macro_area_con_tolleranza(indicatori):
    current_ratio = indicatori.get("current_ratio")
    debt_equity = indicatori.get("debt_equity")
    ebitda_margin = indicatori.get("ebitda_margin")
    utile_netto = indicatori.get("utile_netto")
    investimenti = indicatori.get("investimenti", False)
    crescita_fatturato = indicatori.get("crescita_fatturato", False)
    costi_ambientali = indicatori.get("costi_ambientali", False)

    # Crisi o Risanamento
    if (current_ratio is not None and current_ratio < 1.1 and
        debt_equity is not None and debt_equity > 1.8 and
        ebitda_margin is not None and ebitda_margin < 6 and
        utile_netto is not None and utile_netto < 0):
        return "🔴 Crisi o Risanamento Aziendale"

    # Crescita e Sviluppo
    if (ebitda_margin is not None and ebitda_margin >= 9 and
        utile_netto is not None and utile_netto > 0 and
        debt_equity is not None and 0.3 <= debt_equity <= 2.2 and
        investimenti):
        return "🟠 Crescita e Sviluppo"

    # Espansione / Sostenibilità
    if (ebitda_margin is not None and ebitda_margin >= 14 and
        (costi_ambientali or investimenti or crescita_fatturato)):
        return "🟢 Espansione / Sostenibilità"

    return "⚪️ Non classificato"
