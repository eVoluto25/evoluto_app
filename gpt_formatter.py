def genera_snippet_analisi(data_azienda, indici, macroarea, top_bandi):
    return f"""
📄 ANALISI COMPLETA AZIENDALE

🏢 DATI STRUTTURALI
• Ragione Sociale: {data_azienda['ragione_sociale']}
• Codice ATECO: {data_azienda['codice_ateco']}
• Forma Giuridica: {data_azienda['forma_giuridica']}
• Partita IVA: {data_azienda['partita_iva']}
• Attività Prevalente: {data_azienda['attivita_prevalente']}
• Provincia: {data_azienda['provincia']} – Città: {data_azienda['citta']}
• Data di Costituzione: {data_azienda['data_costituzione']}
• Numero Dipendenti: {data_azienda['dipendenti']}
• Dimensione Impresa: {data_azienda['dimensione']}
• Amministratore: {data_azienda['amministratore']}

📊 INDICATORI ECONOMICI
• Fatturato: €{indici['fatturato']}
• Utile Netto: €{indici['utile_netto']}
• EBITDA: €{indici['ebitda']} (EBITDA Margin: {indici['ebitda_margin']}%)
• Ricerca e Sviluppo: €{indici['ricerca_sviluppo']}
• Costi Ambientali: {indici['costi_ambientali']}

📈 INDICATORI PATRIMONIALI
• Totale Attivo: €{indici['totale_attivo']}
• Liquidità: €{indici['liquidita']}
• Immobilizzazioni: €{indici['immobilizzazioni']}
• Indebitamento: €{indici['indebitamento']}
• Debt/Equity: {indici['debt_equity']}
• Current Ratio: {indici['current_ratio']}
• Interest Coverage Ratio: {indici['interest_coverage']}

💡 STRATEGICI
• Autofinanziamento: €{indici['autofinanziamento']}
• Investimenti recenti: {indici['investimenti']}

🏷️ MACROAREA ASSEGNATA: {macroarea}

🎯 TOP 5 BANDI CONSIGLIATI

{"".join([
f"""- 
📌 *{i+1}. {b['titolo']}*
📎 Agevolazione: {b['forma_agevolazione']}
💰 Spesa Minima Ammessa: €{b['spesa_ammessa']:,}
📈 Beneficio Stimato: {b['impatto_stimato']}
📊 Impatto Simulato: {b['impatto_simulato']}
🧠 Motivazione: {b['motivazione']}

"""
for i, b in enumerate(top_bandi)])}"""

