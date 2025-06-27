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
        if t.lower() in obiettivo.lower():
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
    logger.info(">>> Filtro codice ATECO: %s", codice_ateco)
    logger.info(">>> Filtro dimensione: %s", dimensione)
    logger.info(">>> Macroarea: %s", macroarea)

    # Filtro Regione
    df = df[df["Regioni"].apply(lambda x: regione in x if isinstance(x, list) else False)]
    logger.info(f">>> Dopo filtro Regione: {len(df)} bandi")
    logger.info(f"*** Codici ATECO presenti dopo filtro Regione: {df['Codici_ATECO'].tolist()}")


    # Filtro Codice ATECO (match parziale)
    def match_codice_ateco(lista_ateco, codice):
    """
    Restituisce True se:
    - Il codice ATECO passato è coerente con i codici nel dataset.
    - Oppure se il campo contiene "Tutti i settori".
    """
    if lista_ateco is None:
        return False

    # Se è una stringa unica
    if isinstance(lista_ateco, str):
        if "tutti i settori" in lista_ateco.lower():
            return True
        return False

    codice_normalizzato = codice.strip().replace(".", "").lower()

    for c in lista_ateco:
        if not c:
            continue
        c_norm = c.strip().replace(".", "").lower()
        if "tutti i settori" in c_norm:
            return True
        if c_norm.startswith(codice_normalizzato):
            return True
        if codice_normalizzato.startswith(c_norm):
            return True
        if codice_normalizzato in c_norm:
            return True

    return False

    df = df[df["Codici_ATECO"].apply(lambda x: match_codice_ateco(x, codice_ateco))]
    logger.info(f">>> Dopo filtro Codice ATECO (parziale): {len(df)} bandi")

    # Filtro Dimensione
    df = df[df["Dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)]
    logger.info(f">>> Dopo filtro Dimensione: {len(df)} bandi")

    if df.empty:
        return df

    # Escludi bandi chiusi
    oggi = pd.Timestamp.today()
    df["Data_chiusura_parsed"] = pd.to_datetime(df["Data_chiusura"], errors="coerce")
    df = df[df["Data_chiusura_parsed"] >= oggi]
    logger.info(f">>> Dopo esclusione bandi chiusi: {len(df)} bandi")

    if df.empty:
        return df

    # Priorità Macroarea
    df["Priorita_Macroarea"] = df["Obiettivo_Finalita"].apply(
        lambda x: priorita_macroarea(x, macroarea)
    )

    # Priorità Fondo Perduto
    df["Priorita_Forma"] = df["Forma_agevolazione"].apply(
        lambda x: 1 if x and "fondo perduto" in x.lower() else 2
    )

    # Ordinamento
    df_sorted = df.sort_values(
        by=["Priorita_Macroarea", "Priorita_Forma", "Data_chiusura_parsed"],
        ascending=[True, True, True]
    ).head(max_results)

    # Restituisci solo le colonne richieste
    return df_sorted[["Titolo", "Descrizione", "Obiettivo_Finalita", "Data_chiusura"]]
