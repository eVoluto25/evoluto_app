
import json
import logging
import os

def normalizza_dati(dati: dict) -> dict:
    """
    Converte le chiavi del dizionario 'dati' in chiavi standardizzate
    secondo la mappa 'mappa_alias_variabili.json'. Restituisce un nuovo dizionario.
    """
    alias_path = os.path.join(os.path.dirname(__file__), "mappa_alias_variabili.json")
    try:
        with open(alias_path) as f:
            alias = json.load(f)
        return {alias.get(k, k): v for k, v in dati.items()}
    except Exception as e:
        logging.warning(f"Alias mapping non applicato: {e}")
        return dati # Fallback: restituisce i dati originali
