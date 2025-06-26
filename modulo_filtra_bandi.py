import pandas as pd
import ast
import logging

logger = logging.getLogger(__name__)

def safe_parse_list(val):
    try:
        if isinstance(val, list):
            return val
        if pd.isna(val):
            return []
        return ast.literal_eval(val)
    except Exception as e:
        logger.warning(f"⚠️ Errore parsing campo lista: {val} -> {e}")
        return []

def filtra_bandi(df, codice_ateco=None, regione=None, dimensione=None, forma_agevolazione=None, max_results=5):
    logger.info("🔍 Entrata nella funzione filtra_bandi")

    # Normalizza colonne
    df.columns = [col.lower() for col in df.columns]
    logger.info(f"📊 DataFrame iniziale: {len(df)} righe")

    # Parsa le colonne liste (solo se esistono)
    for col in ["codici_ateco", "regioni", "dimensioni", "forma_agevolazione"]:
        if col in df.columns:
            logger.info(f"🔄 Parsing colonna '{col}'")
            df[col] = df[col].apply(safe_parse_list)

    # Filtro ATECO
    if codice_ateco and "codici_ateco" in df.columns:
        logger.info(f"🔍 Filtro codice ATECO: {codice_ateco}")
        df = df[df["codici_ateco"].apply(lambda lst: "tutti i settori" in lst or codice_ateco in lst)]

    # Filtro Regione
    if regione and "regioni" in df.columns:
        logger.info(f"🔍 Filtro regione: {regione}")
        df = df[df["regioni"].apply(lambda lst: regione in lst)]

    # Filtro Dimensione
    if dimensione and "dimensioni" in df.columns:
        logger.info(f"🔍 Filtro dimensione: {dimensione}")
        df = df[df["dimensioni"].apply(lambda lst: dimensione in lst)]

    # Filtro Forma Agevolazione
    if forma_agevolazione and "forma_agevolazione" in df.columns:
        logger.info(f"🔍 Filtro forma agevolazione: {forma_agevolazione}")
        df = df[df["forma_agevolazione"].apply(lambda lst: forma_agevolazione in lst)]

    colonne_da_restituire = [
        "titolo", "descrizione", "obiettivo_finalita", "data_apertura", "data_chiusura",
        "dimensioni", "forma_agevolazione", "codici_ateco", "regioni", "ambito_territoriale",
        "spesa_ammessa_min", "spesa_ammessa_max", "agevolazione_concedibile_min",
        "agevolazione_concedibile_max", "stanziamento_incentivo"
    ]

    df = df[[col for col in colonne_da_restituire if col in df.columns]]
    df = df.dropna(how="all").head(max_results)

    logger.info(f"✅ Filtro bandi completato: {len(df)} bandi trovati")
    return df.to_dict(orient="records")
