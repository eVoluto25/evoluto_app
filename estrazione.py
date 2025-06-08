import logging
from pipeline import esegui_pipeline

def esegui_pipeline_intermediario(nome_file: str, contenuto: str) -> str:
    """
    Riceve il testo completo dal GPT connector, esegue controlli base e logga tutto prima di avviare la pipeline.
    """

    logging.info(f"📥 Ricevuto input da GPT - Nome file: {nome_file}")
    logging.debug(f"📄 Contenuto ricevuto:\n{contenuto[:1000]}...")  # log parziale per evitare overflow

    if not contenuto.strip():
        logging.warning("⚠️ Il contenuto ricevuto è vuoto.")
        return "Errore: il file PDF caricato non contiene testo leggibile."

    try:
        logging.info("🚀 Avvio analisi tramite pipeline...")
        risultato = esegui_pipeline(nome_file, contenuto)
        logging.info("✅ Analisi completata.")
        return risultato
    except Exception as e:
        logging.error(f"❌ Errore durante l'elaborazione: {str(e)}")
        return f"Errore tecnico durante l'elaborazione del file: {str(e)}"
