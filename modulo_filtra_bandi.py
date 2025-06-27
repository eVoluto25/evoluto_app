import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Mappa macroaree
MAPPATURA_MACROAREA = {
    "innovazione": ["Innovazione", "Digitalizzazione", "Ricerca", "Transizione"],
    "sostegno": ["Sostegno", "Crisi", "Liquidità", "Inclusione"]
}

def priorita_macroarea(obiettivo, macroarea):
    tematiche = MAPPATURA_MACROAREA.get(macroarea, [])
    for t in tematiche:
        if isinstance(obiettivo, str) and t.lower() in obiettivo.lower():
            return 1
    return 2

def filtra_bandi(
    df: pd.DataFrame,
    regione: str,
    codice_ateco: str,
    dimensione: str,
    macroarea: str,
    max_results: int = 5
) -> pd.DataFrame:
    logger.info(">>> Filtro regione: %s", regione)
    logger.info(">>> Filtro dimensione: %s", dimensione)
    logger.info(">>> Macroarea: %s", macroarea)

    # Filtro Regione
    df = df[df["Regioni"].apply(lambda x: regione in x if isinstance(x, list) else False)]
    logger.info(f">>> Dopo filtro Regione: {len(df)} bandi")

    # Filtro Dimensione
    df = df[df["Dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)]
    logger.info(f">>> Dopo filtro Dimensione: {len(df)} bandi")

    if df.empty:
        return df

    # Escludi bandi chiusi
    oggi = pd.Timestamp.today()
    df["Data_chiusura_parsed"] = pd.to_datetime(df["Data_chiusura"], errors="coerce")
    df = df[df["Data_chiusura_parsed"].notnull() & (df["Data_chiusura_parsed"] >= oggi)]
    logger.info(f">>> Dopo esclusione bandi chiusi: {len(df)} bandi")

    if df.empty:
        return df

    # Log bandi aperti a tutti i settori
    df["Aperti_Tutti_Settori"] = df["Codici_ATECO"].apply(
        lambda x: (
            isinstance(x, str) and "tutti i settori" in x.lower()
        ) or (
            isinstance(x, list) and any("tutti i settori" in str(i).lower() for i in x)
        )
    )
    n_tutti_settori = df["Aperti_Tutti_Settori"].sum()
    logger.info(f"✅ Bandi aperti a tutti i settori: {n_tutti_settori}")

    # Priorità Macroarea
    df["Priorita_Macroarea"] = df["Obiettivo_Finalita"].apply(
        lambda x: priorita_macroarea(x, macroarea)
    )

    # Priorità Fondo Perduto
    df["Priorita_Forma"] = df["Forma_agevolazione"].apply(
        lambda x: 1 if isinstance(x, str) and "fondo perduto" in x.lower() else 2
    )

    # Ordinamento
    df_sorted = df.sort_values(
        by=["Priorita_Macroarea", "Priorita_Forma", "Data_chiusura_parsed"],
        ascending=[True, True, True]
    ).head(max_results)

    # Log titoli dei bandi selezionati
    logger.info("✅ Titoli bandi selezionati:")
    for idx, titolo in enumerate(df_sorted["Titolo"].tolist(), start=1):
        logger.info(f"  {idx}. {titolo}")

    # Restituisci solo le colonne richieste
    colonne_restituite = [
        "Titolo",
        "Descrizione",
        "Obiettivo_Finalita",
        "Data_chiusura",
        "Forma_agevolazione",
        "Dimensioni",
        "Regioni",
        "Codici_ATECO",
        "Aperti_Tutti_Settori"
    ]
    colonne_presenti = [col for col in colonne_restituite if col in df_sorted.columns]

    return df_sorted[colonne_presenti]
