import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)

def filtra_bandi(
    df,
    codice_ateco=None,
    regione=None,
    dimensione=None,
    forma_agevolazione=None,
    max_results=5
):
    """
    Filtra i bandi sulla base di codice ATECO, regione, dimensione azienda, forma agevolazione.
    Restituisce solo le colonne rilevanti.
    """

    # 🔧 Normalizza nomi colonne
    df.columns = [col.lower() for col in df.columns]

    # 🔧 Pulisci stringhe sporche (testo con virgolette, spazi, ecc.)
    def pulisci_colonna(col):
        return col.str.replace(r'[\[\]\']', '', regex=True).str.strip()

    for col in ["codici_ateco", "regioni", "dimensioni", "forma_agevolazione"]:
        if col in df.columns and df[col].dtype == object:
            df[col] = df[col].fillna("").astype(str)

    # ✅ Filtro per codice ATECO
    if codice_ateco:
        df = df[df["codici_ateco"].str.contains(codice_ateco, na=False, case=False)]

    # ✅ Filtro per regione
    if regione:
        df = df[df["regioni"].str.contains(regione, na=False, case=False)]

    # ✅ Filtro per dimensione (parsing JSON)
    if dimensione:
        try:
            df["dimensioni"] = df["dimensioni"].apply(
                lambda x: json.loads(x) if isinstance(x, str) else []
            )
        except Exception as e:
            logger.error(f"Errore parsing colonna dimensioni: {e}")
            df["dimensioni"] = [[] for _ in range(len(df))]

        df = df[df["dimensioni"].apply(lambda x: dimensione in x)]

    # ✅ Filtro per forma agevolazione
    if forma_agevolazione:
        df = df[df["forma_agevolazione"].str.contains(forma_agevolazione, na=False, case=False)]

    # 📦 Colonne da restituire
    colonne_da_restituire = [
        "titolo", "descrizione", "obiettivo_finalita",
        "data_apertura", "data_chiusura",
        "dimensioni", "forma_agevolazione",
        "codici_ateco", "regioni", "ambito_territoriale"
    ]
    df = df[[col for col in colonne_da_restituire if col in df.columns]]
    df = df.dropna(how="all").head(max_results)

    return df.to_dict(orient="records")
