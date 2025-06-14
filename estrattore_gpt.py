
import json
from typing import Dict

def estrai_dati_gpt(output_gpt: str) -> Dict:
    """
    Estrae e struttura i dati anagrafici e contabili da una stringa JSON generata da GPT.

    Args:
        output_gpt (str): Stringa JSON restituita da GPT a seguito dell'analisi PDF.

    Returns:
        dict: Dati strutturati con anagrafica e bilancio.
    """
    try:
        dati = json.loads(output_gpt)

        anagrafica = {
            "denominazione": dati.get("denominazione", ""),
            "codice_ateco": dati.get("codice_ateco", ""),
            "regione": dati.get("regione", ""),
            "forma_giuridica": dati.get("forma_giuridica", ""),
            "dipendenti": dati.get("dipendenti", None),
            "fatturato": dati.get("fatturato", None)
        }

        bilancio = {
            "EBITDA": dati.get("EBITDA", None),
            "Utile_Netto": dati.get("utile_netto", None),
            "Cash_Flow_Operativo": dati.get("cash_flow_operativo", None),
            "Quick_Ratio": dati.get("quick_ratio", None),
            "Patrimonio_Netto": dati.get("patrimonio_netto", None),
            "Debiti_finanziari": dati.get("debiti_finanziari", None),
            "Liquidità": dati.get("liquidita", None),
            "Totale_Attivo": dati.get("totale_attivo", None),
            "Ricavi": dati.get("ricavi", None),
            "Costi": dati.get("costi", None)
        }

        return {
            "anagrafica": anagrafica,
            "bilancio": bilancio
        }

    except json.JSONDecodeError:
        raise ValueError("Formato JSON non valido in output GPT.")
