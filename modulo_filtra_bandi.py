
import pandas as pd

def filtra_bandi(df, codice_ateco=None, regione=None, dimensione=None, forma_agevolazione=None, max_results=5):
    """
    Filtra i bandi sulla base di codice ATECO, regione, dimensione azienda e forma agevolazione.
    Restituisce solo le colonne rilevanti.
    """
    if codice_ateco:
        df = df[df["Codici_ATECO"].str.contains(codice_ateco, na=False, case=False)]
    if regione:
        df = df[df["Regioni"].str.contains(regione, na=False, case=False)]
    if dimensione:
        df = df[df["Dimensioni"].str.contains(dimensione, na=False, case=False)]
    if forma_agevolazione:
        df = df[df["Forma_agevolazione"].str.contains(forma_agevolazione, na=False, case=False)]

    colonne_da_restituire = [
        "Titolo", "Descrizione", "Obiettivo_Finalita",
        "Data_apertura", "Data_chiusura",
        "Dimensioni", "Forma_agevolazione",
        "Codici_ATECO", "Regioni", "Ambito_territoriale"
    ]

    df = df[colonne_da_restituire].dropna(how='all').head(max_results)
    return df.to_dict(orient="records")
