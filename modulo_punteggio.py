
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def calcola_punteggi_matching(df_bandi, azienda_codice_ateco, azienda_dimensione, azienda_regione):
    try:
        df = df_bandi.copy()

        def punteggio_ateco(codici):
            if isinstance(codici, str):
                codici_lista = [c.strip() for c in codici.split(';')]
                if 'tutti i settori' in codici.lower():
                    return 10.0
                elif azienda_codice_ateco in codici_lista:
                    return 10.0
                elif any(azienda_codice_ateco[:2] == codice[:2] for codice in codici_lista):
                    return 6.0
            return 0.0

        def punteggio_agevolazione(forme):
            if isinstance(forme, str):
                if "Contributo/Fondo perduto" in forme:
                    return 10.0
                elif "Agevolazione fiscale" in forme:
                    return 6.0
                elif "Prestito/Anticipo rimborsabile" in forme:
                    return 3.0
            return 0.0

        def punteggio_dimensioni(dimensione_bando):
            if pd.isna(dimensione_bando):
                return 0.0
            return 10.0 if azienda_dimensione.lower() in dimensione_bando.lower() else 3.0

        def punteggio_spese(_):
            return 10.0  # Placeholder fino a nuova logica

        def punteggio_regione(territorio):
            if pd.isna(territorio):
                return 0.0
            if azienda_regione.lower() in territorio.lower():
                return 10.0
            elif "nazionale" in territorio.lower():
                return 8.0
            return 0.0

        df["P_ATECO"] = df["Codici_ATECO"].apply(punteggio_ateco)
        df["P_AGEVOL"] = df["Forma_agevolazione"].apply(punteggio_agevolazione)
        df["P_DIM"] = df["Dimensioni"].apply(punteggio_dimensioni)
        df["P_SPESE"] = df.apply(punteggio_spese, axis=1)
        df["P_REGIONE"] = df["Territorio"].apply(punteggio_regione)

        df["PUNTEGGIO_FINALE"] = (
            df["P_ATECO"] * 0.10 +
            df["P_AGEVOL"] * 0.15 +
            df["P_DIM"] * 0.10 +
            df["P_SPESE"] * 0.10 +
            df["P_REGIONE"] * 0.10
        )

        df["PUNTEGGIO_FINALE"] = df["PUNTEGGIO_FINALE"].round(2)

        logging.info("Calcolo punteggi completato.")
        return df.sort_values("PUNTEGGIO_FINALE", ascending=False)

    except Exception as e:
        logging.error(f"Errore nel calcolo dei punteggi: {e}")
        return pd.DataFrame()
