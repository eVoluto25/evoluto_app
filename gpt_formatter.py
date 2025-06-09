def genera_snippet_analisi(data_azienda, indici, macroarea, top_bandi):
    return f"""

📌 TOP 5 BANDI CONSIGLIATI
""" + "\n\n".join([
        f"""🔹 *{i+1}. {b['titolo']}*
• 💼 Agevolazione: {b['forma_agevolazione']}"
• 💰 Spesa Minima Ammessa: €{b['spesa_ammessa']:,}"
• 📈 Beneficio Stimato: {b['impatto_stimato']}"
• 📉 Impatto Simulato: {b['impatto_simulato']}"
• 🧠 Motivazione: {b['motivazione']}"""
       for i, b in enumerate(top_bandi)
    ])
