import logging
logger = logging.getLogger(__name__)

def genera_output_simulazione(risposte_test, bandi_simulati):
    logger.info(f">>> Tipo risposte_test: {type(risposte_test)}")
    logger.info(f">>> Contenuto risposte_test: {risposte_test}")
    
    if hasattr(risposte_test, "dict"):
        risposte_test = risposte_test.dict()

    prime_tre = list(risposte_test.values())[0:3]
    risposta_crisi = prime_tre.count("C")

    if risposta_crisi == 3:
        logger.warning("⚠️ Analisi simulata non disponibile a causa delle risposte ricevute.")
        return {
            "tipo": "simulata",
            "macro_area": None,
            "macro_area_interpretata": "Simulazione non eseguibile",
            "dimensione": None,
            "indice_z_evoluto": bilancio.get("z_score_letter", "C"),
            "indice_z_evoluto_interpretato": bilancio.get("z_score", "Non disponibile"),
            "indice_mcc_evoluto": bilancio.get("mcc_letter", "C"),
            "indice_mcc_evoluto_interpretato": bilancio.get("mcc", "Non disponibile"),
            "bandi_filtrati": [],
            "output_finale": "❌ Simulazione non disponibile: le risposte alle domande non permettono una previsione attendibile di miglioramento.",
            "indici_plus": {}
        }
        
    # Mappatura delle combinazioni a macro aree e indici simulati
    mappa_simulazioni = {
        "espansione": {
            "macro_area": "Espansione e Transizione",
            "mcc_rating": "A",
            "z_score": "A"
        },
        "sviluppo": {
            "macro_area": "Crescita e Sviluppo",
            "mcc_rating": "B",
            "z_score": "B"
        },
        "crisi": {
            "macro_area": "Crisi o Risanamento Aziendale",
            "mcc_rating": "C",
            "z_score": "C"
        }
    }

    risposta_crisi = [
        risposte_test["sostegno_liquidita"],
        risposte_test["sostegno_investimenti"],
        risposte_test["transizione_ecologica"]
    ].count("C")

    if risposta_crisi == 0:
        scenario = "espansione"
    elif risposta_crisi == 1:
        scenario = "sviluppo"
    else:
        scenario = "crisi"

    simulazione = mappa_simulazioni[scenario]
    output = f"\n\n🔄 **Simulazione: scenario migliorato**\n"
    output += f"- Macro Area simulata: **{simulazione['macro_area']}**\n"
    output += f"- MCC simulato: **{simulazione['mcc_rating']}**\n"
    output += f"- Z-Score simulato: **{simulazione['z_score']}**\n"

    output += "\n\n📑 **Top 3 Bandi in caso di miglioramento**\n"
    for i, bando in enumerate(bandi_simulati[:3], 1):
        output += f"\n🔹 **{i}. {bando.get('Titolo', '—')}** (ID: `{bando.get('ID_Incentivo', 'N/D')}`)\n"
        output += f"- 🎯 Obiettivo: {bando.get('Obiettivo_finalita', '--')}\n"
        output += f"- 💶 Spesa ammessa max: {bando.get('Spesa_Ammessa_max', '--')} €\n"
        output += f"- 🧮 Agevolazione concedibile: {bando.get('Agevolazione_Concedibile_max', '--')} €\n"
        output += f"- 🧾 Forma agevolazione: {bando.get('Forma_agevolazione', '--')}\n"
        output += f"- ⏳ Scadenza: {bando.get('Data_chiusura', '--')}\n"
        dettagli = bando.get("dettagli_gpt", {})
        output += f"- 📋 Dettagli: {dettagli.get('Descrizione', '—')}\n"
        output += f"- 🗓️ Note di apertura/chiusura: {dettagli.get('Note_di_apertura_chiusura', '—')}\n"
        output += f"- 🏢 Tipologia soggetto: {dettagli.get('Tipologia_Soggetto', '—')}\n"
        output += f"- 📊 Stanziamento incentivo: {dettagli.get('Stanziamento_incentivo', '—')} €\n"
        output += f"- 🌐 Verifica online: {dettagli.get('Link_istituzionale', '—')}\n"

    return output
