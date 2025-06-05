
def genera_output_gpt(azienda, bandi_ordinati):
    output = []

    output.append(f"📄 Report Analisi Aziendale per {azienda.get('partita_iva', 'N/D')}")
    output.append(f"🧾 Forma Giuridica: {azienda.get('forma_giuridica', 'N/D')}")
    output.append(f"📍 Codice ATECO: {azienda.get('codice_ateco', 'N/D')}")
    output.append(f"🏙️ Attività Prevalente: {azienda.get('attivita_prevalente', 'N/D')}")
    output.append(f"📌 Provincia: {azienda.get('provincia', 'N/D')}, Città: {azienda.get('citta', 'N/D')}")
    output.append(f"👤 Amministratore: {azienda.get('amministratore', 'N/D')}")
    output.append(f"🗓️ Anno Fondazione: {azienda.get('anno_fondazione', 'N/D')}")
    output.append(f"👥 Dipendenti: {azienda.get('numero_dipendenti', 'N/D')}")

    output.append("\n📊 Indicatori Finanziari")
    output.append(f"• Fatturato Annuo: €{azienda.get('fatturato_annuo', 'N/D')}")
    output.append(f"• Utile Netto: €{azienda.get('utile_netto', 'N/D')}")
    output.append(f"• EBITDA: €{azienda.get('ebitda', 'N/D')}")
    output.append(f"• EBITDA Margin: {azienda.get('ebitda_margin', 'N/D')}%")
    output.append(f"• Costi R&S: €{azienda.get('spese_r_s', 'N/D')}")
    output.append(f"• Costi Ambientali: €{azienda.get('costi_ambientali', 'N/D')}")
    output.append(f"• Totale Attivo: €{azienda.get('totale_attivo', 'N/D')}")
    output.append(f"• Disponibilità liquide: €{azienda.get('disponibilita_liquide', 'N/D')}")
    output.append(f"• Immobilizzazioni: €{azienda.get('immobilizzazioni', 'N/D')}")
    output.append(f"• Indebitamento Totale: €{azienda.get('indebitamento', 'N/D')}")
    output.append(f"• Debt/Equity Ratio: {azienda.get('debt_equity_ratio', 'N/D')}")
    output.append(f"• Current Ratio: {azienda.get('current_ratio', 'N/D')}")
    output.append(f"• Interest Coverage Ratio: {azienda.get('interest_coverage_ratio', 'N/D')}")
    output.append(f"• Capacità di Autofinanziamento: €{azienda.get('capacita_autofinanziamento', 'N/D')}")
    output.append(f"• Investimenti Recenti: €{azienda.get('investimenti_recenti', 'N/D')}")

    output.append("\n🔍 Posizionamento Strategico")
    output.append(f"• Crisi o Risanamento: {azienda.get('area_crisi_risanamento', 'N/D')}")
    output.append(f"• Crescita e Sviluppo: {azienda.get('area_crescita_sviluppo', 'N/D')}")
    output.append(f"• Espansione e Transizione: {azienda.get('area_espansione_transizione', 'N/D')}")

    output.append("\n🎯 Incentivi compatibili (massimo 10):")
    for i, bando in enumerate(bandi_ordinati[:10], start=1):
        output.append(f"{i}. {bando['Titolo']}")
        output.append(f"   🔗 {bando['Link_istituzionale']}")
        output.append(f"   📈 Valutazione: {bando['valutazione 0-100']}/100")
        output.append(f"   📊 Probabilità: {bando['probabilità']}")
        output.append(f"   📍 Territorio: {bando['Ambito_territoriale']}")
        output.append("")

    return "\n".join(output)
