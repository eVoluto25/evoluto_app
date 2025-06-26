import pandas as pd

def normalizza_valore(valore):
    if not isinstance(valore, str):
        return ""
    return (
        valore.replace(".", "")
              .replace(";", ",")
              .replace(":", ",")
              .strip()
              .lower()
    )

def filtra_bandi(df, codice_ateco=None, regione=None, dimensione=None, forma_agevolazione=None, max_results=5):
    """
    Filtra i bandi sulla base di codice ATECO, regione, dimensione azienda, forma agevolazione.
    Restituisce solo le colonne rilevanti.
    """
    # Normalizza tutte le colonne a lowercase
    df.columns = [col.lower() for col in df.columns]

    # Filtro codice ATECO
    if codice_ateco:
        codice_ateco = normalizza_valore(codice_ateco)
        df = df[df["codici_ateco"].apply(lambda x: codice_ateco in normalizza_valore(x))]

    # Filtro regione
    if regione:
        regione = normalizza_valore(regione)
        df = df[df["regioni"].apply(lambda x: regione in normalizza_valore(x))]

    # Filtro dimensione azienda
    if dimensione:
        dimensione = normalizza_valore(dimensione)
        df = df[df["dimensioni"].apply(lambda x: dimensione in normalizza_valore(x))]

    # Filtro forma agevolazione
    if forma_agevolazione:
        forma_agevolazione = normalizza_valore(forma_agevolazione)
        df = df[df["forma_agevolazione"].apply(lambda x: forma_agevolazione in normalizza_valore(x))]

    # Colonne da restituire
    colonne_da_restituire = [
        "titolo", "descrizione", "obiettivo_finalita",
        "data_apertura", "data_chiusura",
        "dimensioni", "forma_agevolazione",
        "codici_ateco", "regioni", "ambito_territoriale"
    ]
    
    df = df[[col for col in colonne_da_restituire if col in df.columns]]
    df = df.dropna(how="all").head(max_results)

    return df.to_dict(orient="records")
