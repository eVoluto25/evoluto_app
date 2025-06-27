import logging
import pandas as pd

logger = logging.getLogger(__name__)

def filtra_bandi(
    df: pd.DataFrame,
    regione: str,
    codice_ateco: str,
    dimensione: str,
    forma_agevolazione: str,
    max_results: int = 5
) -> pd.DataFrame:
    logger.info(">>> Filtro regione: %s", regione)
    logger.info(">>> Filtro codice ATECO: %s", codice_ateco)
    logger.info(">>> Filtro dimensione: %s", dimensione)
    logger.info(">>> Filtro forma agevolazione: %s", forma_agevolazione)

    # ✅ Filtra per regione
    df_regioni = df[df["Regioni"].apply(lambda x: regione in x if isinstance(x, list) else False)]
    logger.info(f">>> Bandi dopo filtro regione: {len(df_regioni)}")

    # ✅ Filtra per codice ATECO
    df_ateco = df_regioni[df_regioni["Codici_ATECO"].apply(lambda x: codice_ateco in x if isinstance(x, list) else False)]
    logger.info(f">>> Bandi dopo filtro codice ATECO: {len(df_ateco)}")

    # ✅ Filtra per dimensione
    df_dimensione = df_ateco[df_ateco["Dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)]
    logger.info(f">>> Bandi dopo filtro dimensione: {len(df_dimensione)}")

    # ✅ Filtra per forma agevolazione (se presente)
    if forma_agevolazione:
        df_forma = df_dimensione[df_dimensione["Forma_agevolazione"] == forma_agevolazione]
        logger.info(f">>> Bandi dopo filtro forma agevolazione: {len(df_forma)}")
    else:
        df_forma = df_dimensione
        logger.info(">>> Nessun filtro forma agevolazione applicato.")

    # ✅ Ordina o limita i risultati
    df_risultato = df_forma.head(max_results)

    return df_risultato
