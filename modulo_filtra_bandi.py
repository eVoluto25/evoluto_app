import pandas as pd

def filtra_bandi(df, codice_ateco=None, regione=None, dimensione=None, forma_agevolazione=None, max_results=5):
    """
    Filtra i bandi sulla base di codice ATECO, regione, dimensione azienda.
    Restituisce solo le colonne rilevanti.
    """
    # Normalizza nomi colonne a lowercase
    df.columns = [col.lower() for col in df.columns]

    print(f">>> Codice ATECO richiesto: {codice_ateco}")
    print(f">>> Esempi da colonna codici_ateco:")
    print(df["codici_ateco"].dropna().unique()[:10])

    if codice_ateco:
        df = df[df["codici_ateco"].str.contains(codice_ateco, na=False, case=False)]
    if regione:
        df = df[df["regioni"].str.contains(regione, na=False, case=False)]
    if dimensione:
        df = df[df["dimensioni"].str.contains(dimensione, na=False, case=False)]

    colonne_da_restituire = [
        "titolo", "descrizione", "obiettivo_finalita",
        "data_apertura", "data_chiusura",
        "dimensioni", "forma_agevolazione",
        "codici_ateco", "regioni", "ambito_territoriale"
    ]

    df = df[[col for col in colonne_da_restituire if col in df.columns]]
    df = df.dropna(how="all").head(max_results)

    return df.to_dict(orient="records")
