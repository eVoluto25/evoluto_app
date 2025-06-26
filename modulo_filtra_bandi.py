import pandas as pd
import ast
import logging

logger = logging.getLogger(__name__)

def filtra_bandi(df, codice_ateco=None, regione=None, dimensione=None, forma_agevolazione=None, max_results=5):
    """
    Filtra i bandi sulla base di codice ATECO, regione, dimensione azienda, forma di agevolazione.
    Restituisce solo le colonne rilevanti.
    """

    logger.info("🔍 Avvio funzione filtra_bandi()")

    df.columns = [col.lower() for col in df.columns]

    def safe_parse(val):
        try:
            return ast.literal_eval(val) if isinstance(val, str) else []
        except Exception as e:
            logger.warning(f"⚠️ Errore parsing campo lista: {val} -> {e}")
            return []

    for col in ["dimensioni", "codici_ateco", "regioni", "forma_agevolazione"]:
        if col in df.columns:
            logger.info(f"🧹 Parsing colonna '{col}'")
            df[col] = df[col].apply(safe_parse)
        else:
            logger.warning(f"🚫 Colonna '{col}' non trovata nel DataFrame")

    logger.info(f"📊 DataFrame iniziale: {len(df)} righe")

    if codice_ateco:
        df = df[df["codici_ateco"].apply(lambda lst: codice_ateco in lst or "Tutti i settori economici ammissibili a ricevere aiuti" in lst)]
        logger.info(f"✅ Filtro codice ATECO: {codice_ateco} → {len(df)} righe")

    if regione:
        df = df[df["regioni"].apply(lambda lst: regione in lst or "Tutte le regioni" in lst)]
        logger.info(f"✅ Filtro regione: {regione} → {len(df)} righe")

    if dimensione:
        df = df[df["dimensioni"].apply(lambda lst: dimensione in lst)]
        logger.info(f"✅ Filtro dimensione: {dimensione} → {len(df)} righe")

    if forma_agevolazione:
        df = df[df["forma_agevolazione"].apply(lambda lst: forma_agevolazione in lst)]
        logger.info(f"✅ Filtro forma agevolazione: {forma_agevolazione} → {len(df)} righe")

    colonne_da_restituire = [
        "titolo", "descrizione", "obiettivo_finalita",
        "data_apertura", "data_chiusura", "dimensioni",
        "forma_agevolazione", "codici_ateco", "regioni",
        "ambito_territoriale", "spesa_ammessa_min", "spesa_ammessa_max",
        "agevolazione_concedibile_min", "agevolazione_concedibile_max",
        "stanziamento_incentivo"
    ]

    df = df[[col for col in colonne_da_restituire if col in df.columns]]
    df = df.dropna(how="all").head(max_results)

    logger.info(f"🏁 Filtro completato: {len(df)} righe finali restituite")

    return df.to_dict(orient="records")
