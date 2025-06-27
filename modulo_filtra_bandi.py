import logging
import pandas as pd
from criteri_scoring import MCC_RATING_PUNTEGGIO, Z_SCORE_PUNTEGGIO, motivazione_solidita

logger = logging.getLogger(__name__)

def filtra_bandi(
    df: pd.DataFrame,
    regione: str,
    dimensione: str,
    obiettivo_preferenziale: str,
    mcc_rating: str,
    z_score: float,
    max_results: int = 5
) -> list:
    logger.info(">>> Filtro regione: %s", regione)
    logger.info(">>> Filtro dimensione: %s", dimensione)
    logger.info(">>> Obiettivo preferenziale: %s", obiettivo_preferenziale)
    logger.info(">>> MCC: %s | Z-Score: %s", mcc_rating, z_score)

    # Filtro Regione
    df = df[df["Regioni"].apply(lambda x: regione in x if isinstance(x, list) else False)]
    logger.info(f">>> Dopo filtro Regione: {len(df)} bandi")

    # Filtro Dimensione
    df = df[df["Dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)]
    logger.info(f">>> Dopo filtro Dimensione: {len(df)} bandi")

    if df.empty:
        return []

    # Escludi bandi chiusi
    oggi = pd.Timestamp.today()
    df["Data_chiusura_parsed"] = pd.to_datetime(df["Data_chiusura"], errors="coerce")
    df = df[df["Data_chiusura_parsed"].notnull() & (df["Data_chiusura_parsed"] >= oggi)]
    logger.info(f">>> Dopo esclusione bandi chiusi: {len(df)} bandi")

    if df.empty:
        return []

    # Priorità Obiettivo Preferito
    def priorita_obiettivo(obiettivo_bando, obiettivo_scelto):
        if (
            isinstance(obiettivo_bando, str)
            and isinstance(obiettivo_scelto, str)
            and obiettivo_scelto.lower() in obiettivo_bando.lower()
        ):
            return 1
        return 2

    df["Priorita_Obiettivo"] = df["Obiettivo_Finalita"].apply(
        lambda x: priorita_obiettivo(x, obiettivo_preferenziale)
    )

    # Punteggio solidità
    mcc_punteggio = MCC_RATING_PUNTEGGIO.get(mcc_rating.upper(), 5)
    z_punteggio = punteggio_zscore(z_score)
    media_punteggio = (mcc_punteggio + z_punteggio) / 2
    coerenza = livello_coerenza_solidita(media_punteggio)
    motivazione = motivazione_solidita(media_punteggio)

    # Ordinamento
    df_sorted = df.sort_values(
        by=["Priorita_Obiettivo", "Data_chiusura_parsed"],
        ascending=[True, True]
    ).head(max_results)

    # Log titoli bandi
    logger.info("✅ Titoli bandi selezionati:")
    for idx, titolo in enumerate(df_sorted["Titolo"].tolist(), start=1):
        logger.info(f"  {idx}. {titolo}")

    # Costruisci lista di dizionari da restituire
    risultati = []
    for _, row in df_sorted.iterrows():
        risultati.append({
            "titolo": row.get("Titolo", ""),
            "descrizione": row.get("Descrizione", ""),
            "data": str(row.get("Data_chiusura", "")),
            "coerenza_solidita": coerenza,
            "motivazione": motivazione,
            "descrizione": row.get("Descrizione", "")
        })

    return risultati
