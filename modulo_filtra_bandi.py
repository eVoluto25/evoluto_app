import logging
import pandas as pd

logger = logging.getLogger(__name__)

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

# Funzione per calcolare il punteggio Z-Score
def punteggio_zscore(z_score: float) -> int:
    for min_val, max_val, score in Z_SCORE_PUNTEGGIO:
        if min_val <= z_score <= max_val:
            return score
    return 5

# Funzione per assegnare livello coerenza solidità
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

# Funzione per riassumere la descrizione in max 30 parole
def riassunto_30_parole(testo):
    """
    Restituisce le prime 30 parole del testo.
    Se il testo ha meno di 30 parole, torna intero.
    Nessuna dipendenza esterna.
    """
    if not testo:
        return ""
    parole = testo.split()
    if len(parole) <= 30:
        return testo
    return " ".join(parole[:30]) + "..."

# Funzione principale di filtraggio bandi
def filtra_bandi(
    df: pd.DataFrame,
    regione: str,
    dimensione: str,
    obiettivo_preferenziale: str,
    mcc_rating: str,
    z_score: float,
    max_results: int = 20
) -> list:
    logger.info(">>> Filtro regione: %s", regione)
    logger.info(">>> Filtro dimensione: %s", dimensione)
    logger.info(">>> Obiettivo preferenziale: %s", obiettivo_preferenziale)
    logger.info(">>> MCC: %s | Z-Score: %s", mcc_rating, z_score)

    # Calcola punteggi solidità
    mcc_punteggio = MCC_RATING_PUNTEGGIO.get(mcc_rating.upper(), 5)
    z_punteggio = punteggio_zscore(z_score)
    media_punteggio = (mcc_punteggio + z_punteggio) / 2
    coerenza = livello_coerenza_solidita(media_punteggio)
    motivazione = motivazione_solidita(media_punteggio)

    # Determina solidità critica
    solidita_critica = (
        mcc_rating.upper() in ["CCC", "B"]
        and z_score <= 0
    )
    if solidita_critica:
        logger.info(">>> Solidità critica: filtreremo solo bandi di sostegno.")
    else:
        logger.info(">>> Solidità non critica.")

    # Escludi bandi con scadenza entro 60 giorni
    oggi = pd.Timestamp.today()
    df["Data_chiusura_parsed"] = pd.to_datetime(df["Data_chiusura"], errors="coerce")
    scadenza_limite = oggi + pd.Timedelta(days=60)
    df = df[
        df["Data_chiusura_parsed"].notnull()
        & (df["Data_chiusura_parsed"] >= scadenza_limite)
    ]
    if df.empty:
        logger.info(">>> Nessun bando con scadenza oltre 60 giorni.")
        return []

    # Funzione match regione
    def match_regione(campo, regione):
        if campo is None:
            return False
        if isinstance(campo, list):
            return regione in campo or "Tutte le regioni" in campo
        if isinstance(campo, str):
            campo_norm = campo.lower()
            return (regione.lower() in campo_norm) or ("tutte le regioni" in campo_norm)
        return False

    # Filtro solidità critica
    if solidita_critica:
        df_selected = df[
            df["Regioni"].apply(lambda x: match_regione(x, regione))
            &
            df["Obiettivo_Finalita"].apply(
                lambda x: "sostegno" in x.lower() if isinstance(x, str) else False
            )
            &
            df["Dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)
        ]
        logger.info(">>> Filtro solidità critica: trovati %s bandi.", len(df_selected))
    else:
        # Fase 1: Regione + Obiettivo preferenziale
        df_step1 = df[
            df["Regioni"].apply(lambda x: match_regione(x, regione))
            &
            df["Obiettivo_Finalita"].apply(
                lambda x: obiettivo_preferenziale.lower() in x.lower() if isinstance(x, str) else False
            )
            &
            df["Dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)
        ]
        if not df_step1.empty:
            df_selected = df_step1.copy()
            logger.info(">>> Fase 1: trovati %s bandi.", len(df_selected))
        else:
            # Fase 2: Regione con qualsiasi obiettivo
            df_step2 = df[
                df["Regioni"].apply(lambda x: match_regione(x, regione))
                &
                df["Dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)
            ]
            if not df_step2.empty:
                df_selected = df_step2.copy()
                logger.info(">>> Fase 2: trovati %s bandi.", len(df_selected))
            else:
                # Fase 3: Tutti i bandi con qualsiasi regione
                df_selected = df[
                    df["Dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)
                ]
                logger.info(">>> Fase 3: trovati %s bandi.", len(df_selected))

    if df_selected.empty:
        return []

    # Priorità Obiettivo
    df_selected["Priorita_Obiettivo"] = df_selected["Obiettivo_Finalita"].apply(
        lambda x: 1 if obiettivo_preferenziale.lower() in str(x).lower() else 2
    )
    df_selected["Punteggio_Solidita"] = media_punteggio

    # Ordinamento
    df_sorted = df_selected.sort_values(
        by=["Priorita_Obiettivo", "Punteggio_Solidita", "Data_chiusura_parsed"],
        ascending=[True, False, True]
    ).head(max_results)

    # Log titoli
    logger.info("✅ Titoli bandi selezionati:")
    for idx, titolo in enumerate(df_sorted["Titolo"].tolist(), start=1):
        logger.info(f"  {idx}. {titolo}")

    # Output
    risultati = []
    for _, row in df_sorted.iterrows():
        descrizione_ridotta = riassunto_50_parole(row.get("Descrizione", ""))
        risultati.append({
            "titolo": row.get("Titolo", ""),
            "data": str(row.get("Data_chiusura", "")),
            "coerenza_solidita": coerenza,
            "motivazione": motivazione,
            "forma_agevolazione": row.get("Forma_agevolazione", ""),
            "costi_ammessi": row.get("Costi_Ammessi", ""),
            "descrizione": descrizione_ridotta
        })

    return risultati
