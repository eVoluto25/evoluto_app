import logging
import pandas as pd

# Dizionario di punteggio MCC
MCC_RATING_PUNTEGGIO = {
    "AAA": 10,
    "AA": 9,
    "A": 8,
    "BBB": 7,
    "BB": 6,
    "B": 4,
    "CCC": 2
}

# Intervalli di punteggio Z-Score
Z_SCORE_PUNTEGGIO = [
    (-9999, 0, 2),
    (0, 1.8, 4),
    (1.8, 2.99, 7),
    (3, 9999, 10)
]

logger = logging.getLogger(__name__)

# Funzione per calcolare il punteggio Z-Score
def punteggio_zscore(z_score: float) -> int:
    for min_val, max_val, score in Z_SCORE_PUNTEGGIO:
        if min_val <= z_score <= max_val:
            return score
    return 5

# Funzione per assegnare il livello di coerenza solidità
def livello_coerenza_solidita(punteggio: float) -> str:
    if punteggio >= 9:
        return "Eccellente 🟢"
    elif punteggio >= 7:
        return "Alta 🟢"
    elif punteggio >= 5:
        return "Media 🟡"
    elif punteggio >= 3:
        return "Bassa 🟠"
    else:
        return "Critica 🔴"

# Funzione per generare la motivazione
def motivazione_solidita(punteggio: float) -> str:
    if punteggio >= 9:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda presenta una solidità ECCELLENTE. "
            "Il bando è pienamente coerente con la struttura economico-finanziaria e rappresenta un'opportunità prioritaria di sviluppo. 🟢"
        )
    elif punteggio >= 7:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda mostra una solidità ALTA. "
            "Il bando è coerente con le performance aziendali e può supportare investimenti strategici. 🟢"
        )
    elif punteggio >= 5:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda possiede una solidità MEDIA. "
            "La partecipazione al bando è possibile, ma si consiglia un'attenta valutazione della capacità di cofinanziamento. 🟡"
        )
    elif punteggio >= 3:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda evidenzia una solidità BASSA. "
            "Il bando potrebbe presentare criticità in fase di candidatura, si raccomanda cautela. 🟠"
        )
    else:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda mostra una solidità CRITICA. "
            "Il bando selezionato non è consigliato senza interventi di miglioramento della situazione finanziaria. 🔴"
        )

# Funzione principale di filtraggio bandi
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
    def match_regione(campo, regione):
        if campo is None:
            return False
        if isinstance(campo, list):
            return regione in campo or "Tutte le regioni" in campo
        if isinstance(campo, str):
            campo_norm = campo.lower()
            return (regione.lower() in campo_norm) or ("tutte le regioni" in campo_norm)
        return False

    df = df[df["Regioni"].apply(lambda x: match_regione(x, regione))]

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

    # Calcola punteggio solidità e motivazione
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
            "data": str(row.get("Data_chiusura", "")),
            "coerenza_solidita": coerenza,
            "motivazione": motivazione,
            "forma_agevolazione": row.get("Forma_agevolazione", ""),
            "costi_ammessi": row.get("Costi_Ammessi", ""),
            "descrizione": row.get("Descrizione", "")
        })

    return risultati
