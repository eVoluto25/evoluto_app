from pipeline import avvia_pipeline

def esegui_pipeline(nome_file, contenuto):
    """
    Riceve il testo completo del file PDF caricato via GPT.
    Non filtra, non analizza, non modifica nulla.
    Passa tutto il contenuto a pipeline.avvia_pipeline per l'elaborazione.
    """
    return avvia_pipeline(nome_file, contenuto)
