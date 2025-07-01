import logging
import pandas as pd

logger = logging.getLogger(__name__)

MCC_RATING_PUNTEGGIO = {
    "AAA": 10,
    "AA": 9,
    "A": 8,
    "BBB": 7,
    "BB": 6,
    "B": 4,
    "CCC": 2
}

Z_SCORE_PUNTEGGIO = [
    (-9999, 0, 2),
    (0, 1.8, 4),
    (1.8, 2.99, 7),
    (3, 9999, 10)
]

def punteggio_zscore(z_score: float) -> int:
    for min_val, max_val, score in Z_SCORE_PUNTEGGIO:
        if min_val <= z_score <= max_val:
            return score
    return 5

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

def riassunto_50_parole(testo):
    if not testo:
        return ""
    parole = testo.split()
    if len(parole) <= 50:
        return testo
    return " ".join(parole[:50]) + "..."

def filtra_bandi(
    df: pd.DataFrame,
    regione: str,
    dimensione: str,
    obiettivo_preferenziale: str,
    mcc_rating: str,
    z_score: float,
    max_results: int = 50
) -> list:
    logger.info(">>> Filtro regione: %s", regione)
    logger.info(">>> Filtro dimensione: %s", dimensione)
    logger.info(">>> Obiettivo preferenziale: %s", obiettivo_preferenziale)
    logger.info(">>> MCC: %s | Z-Score: %s", mcc_rating, z_score)

    # Pulizia e normalizzazione colonne
    df["regioni_clean"] = df["Regioni"].astype(str).str.strip().str.lower()
    df["dimensioni_clean"] = df["Dimensioni"].astype(str).str.strip().str.lower()
    df["obiettivo_clean"] = df["Obiettivo_Finalita"].astype(str).str.strip().str.lower()
    df["titolo_clean"] = df["Titolo"].astype(str).str.strip()
    df["descrizione_clean"] = df["Descrizione"].astype(str).str.strip()

    dimensione_clean = dimensione.strip().lower()
    obiettivo_clean = obiettivo_preferenziale.strip().lower()

    # Calcola punteggi solidità
    mcc_punteggio = MCC_RATING_PUNTEGGIO.get(mcc_rating.upper(), 5)
    z_punteggio = punteggio_zscore(z_score)
    media_punteggio = (mcc_punteggio + z_punteggio) / 2

    coerenza = livello_coerenza_solidita(media_punteggio)
    motivazione = motivazione_solidita(media_punteggio)

    solidita_critica = (
        mcc_rating.upper() in ["CCC", "B"]
        and z_score <= 0
    )
    if solidita_critica:
        logger.info(">>> Solidità critica: filtreremo solo bandi di sostegno.")
    else:
        logger.info(">>> Solidità non critica.")

    oggi = pd.Timestamp.today()
    df["Data_chiusura_parsed"] = pd.to_datetime(df["data_chiusura_clean"], errors="coerce")
    scadenza_limite = oggi + pd.Timedelta(days=45)
    df = df[
        (df["Data_chiusura_parsed"].isna())
        | (df["Data_chiusura_parsed"] >= scadenza_limite)
    ]
    if df.empty:
        logger.info(">>> Nessun bando con scadenza oltre 45 giorni.")
        return []

    def match_regione(campo, regione):
        if campo is None:
            return False
        if isinstance(campo, list):
            return regione in campo or "tutte le regioni" in campo
        if isinstance(campo, str):
            campo_norm = campo.lower()
            return (regione.lower() in campo_norm) or ("tutte le regioni" in campo_norm)
        return False

    if solidita_critica:
        df_selected = df[
            df["regioni_clean"].apply(lambda x: match_regione(x, regione))
            &
            df["obiettivo_clean"].apply(
                lambda x: "sostegno" in x if isinstance(x, str) else False
            )
            &
            (df["dimensioni_clean"] == dimensione_clean)
        ]
        logger.info(">>> Filtro solidità critica: trovati %s bandi.", len(df_selected))
    else:
        df_step1 = df[
            df["regioni_clean"].apply(lambda x: match_regione(x, regione))
            &
            df["obiettivo_clean"].apply(
                lambda x: obiettivo_clean in x if isinstance(x, str) else False
            )
            &
            (df["dimensioni_clean"] == dimensione_clean)
        ]
        if not df_step1.empty:
            df_selected = df_step1.copy()
            logger.info(">>> Fase 1: trovati %s bandi.", len(df_selected))
        else:
            df_step2 = df[
                df["regioni_clean"].apply(lambda x: match_regione(x, regione))
                &
                (df["dimensioni_clean"] == dimensione_clean)
            ]
            if not df_step2.empty:
                df_selected = df_step2.copy()
                logger.info(">>> Fase 2: trovati %s bandi.", len(df_selected))
            else:
                df_selected = df[
                    (df["dimensioni_clean"] == dimensione_clean)
                ]
                logger.info(">>> Fase 3: trovati %s bandi.", len(df_selected))

    if df_selected.empty:
        return []

    df_selected["Priorita_Obiettivo"] = df_selected["obiettivo_clean"].apply(
        lambda x: 1 if obiettivo_clean in str(x) else 2
    )
    df_selected["Punteggio_Solidita"] = media_punteggio

    df_sorted = df_selected.sort_values(
        by=["Priorita_Obiettivo", "Punteggio_Solidita", "Data_chiusura_parsed"],
        ascending=[True, False, True]
    ).head(max_results)

    logger.info("✅ Titoli bandi selezionati:")
    for idx, titolo in enumerate(df_sorted["titolo_clean"].tolist(), start=1):
        logger.info(f"  {idx}. {titolo}")

    risultati = []
    for _, row in df_sorted.iterrows():
        punteggio = row.get("Punteggio_Solidita", 0)
        motivazione = motivazione_solidita(punteggio)
        livello_coerenza = livello_coerenza_solidita(punteggio)

        descrizione_ridotta = riassunto_50_parole(row.get("descrizione_clean", ""))

        data_chiusura = row.get("data_chiusura_clean", "")
        if not data_chiusura or data_chiusura.strip() == "":
            data_chiusura = "bando disponibile fino ad esaurimento fondi. Verificare residuo stanziamento."

        risultati.append({
            "titolo": row.get("titolo_clean", ""),
            "data": data_chiusura,
            "coerenza_solidita": livello_coerenza,
            "obiettivo_finalita": row.get("obiettivo_clean", ""),
            "percentuale_ammissibilità": row.get("percentuale_ammissibilità", ""),
            "motivazione": motivazione,
            "forma_agevolazione": row.get("forma_agevolazione_clean", ""),
            "costi_ammessi": row.get("Costi_Ammessi", ""),
            "descrizione": descrizione_ridotta
        })

    return risultati
