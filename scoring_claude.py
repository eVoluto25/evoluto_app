def calcola_punteggio_bando(bando, azienda):
    punteggio = 0
    log = {}

    # 1. Solidità finanziaria (50%)
    solidita = 0
    ebitda = azienda.get("ebitda", 0)
    utile_netto = azienda.get("utile_netto", 0)
    debiti_finanziari = azienda.get("debiti_finanziari", 0)
    patrimonio_netto = azienda.get("patrimonio_netto", 0)
    z_score = azienda.get("z_score", None)
    mcc_rating = azienda.get("mcc_rating", None)

    # EBITDA positivo
    if ebitda > 0:
        solidita += 1
        log["ebitda_positivo"] = 1
    else:
        log["ebitda_positivo"] = 0

    # Utile positivo
    if utile_netto > 0:
        solidita += 1
        log["utile_positivo"] = 1
    else:
        log["utile_positivo"] = 0

    # Debt/Equity
    debt_equity = debiti_finanziari / patrimonio_netto if patrimonio_netto else None
    if debt_equity is not None and 0.5 <= debt_equity <= 2:
        solidita += 1
        log["debt_equity_ok"] = 1
    else:
        log["debt_equity_ok"] = 0

    # Z-score critico
    if z_score is not None and z_score < 1.8:
        solidita -= 1
        log["z_score_critico"] = -1
    else:
        log["z_score_critico"] = 0

    # MCC critico
    if mcc_rating is not None and mcc_rating >= 4:
        solidita -= 1
        log["mcc_critico"] = -1
    else:
        log["mcc_critico"] = 0

    punteggio += max(0, solidita) * 50 / 5

    # 2. Forma dell’agevolazione (25%)
    forma = bando.get("forma_agevolazione", "").lower()
    if "fondo perduto" in forma:
        punteggio += 25
        log["forma_agevolazione"] = "fondo perduto"
    elif "credito d’imposta" in forma:
        punteggio += 12.5
        log["forma_agevolazione"] = "credito d’imposta"
    elif "finanziamento" in forma:
        punteggio += 6.25
        log["forma_agevolazione"] = "finanziamento"
    else:
        log["forma_agevolazione"] = "altro"

    return round(punteggio, 2), log

def genera_output_finale_claude(claude_output, macro_area, dimensione, mcc, z_score):
    output = f"""
📂 Macro Area Assegnata: {macro_area}
🏷 Dimensione Impresa: {dimensione}
🔐 MCC Rating: {mcc}
📉 Z-Score stimato: {z_score}

📋 eVoluto ha analizzato 25 bandi pubblici. Ecco i 3 più coerenti con la tua struttura aziendale (punteggio ≥ 80):
"""

    for i, bando in enumerate(claude_output, 1):
        output += f"""
{i}. 🏆 **{bando.get('Titolo', 'Senza titolo')}**
   - 🎯 Obiettivo: {bando.get('Obiettivo_finalita', '-')}
   - 💬 Motivazione: {bando.get('Motivazione', '-')}
   - 💰 Spesa ammessa max: {bando.get('Spesa_Ammessa_max', '-')}
   - 🎁 Agevolazione concedibile: {bando.get('Agevolazione_Concedibile_max', '-')}
   - 🧾 Forma agevolazione: {bando.get('Forma_agevolazione', '-')}
   - ⏳ Scadenza: {bando.get('Data_chiusura', '-')}
"""

    output += """
📌 Puoi usare queste informazioni per valutare la candidatura ai bandi più adatti.
"""

    return output
