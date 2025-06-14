# processa_azienda.py – flusso completo: indici + macroarea

from calcolo_indici_finanziari import analizza_indici
from macroarea_logica import valuta_macroarea_logica

def processa_azienda(dati: dict) -> dict:
    bilancio = dati.get("bilancio", {})
    anagrafica = dati.get("anagrafica", {})

    # 1. Calcolo indici
    indici = analizza_indici({"bilancio": bilancio})

    # 2. Macroarea
    macroarea_result = valuta_macroarea_logica({
        **indici,
        **bilancio  # servono utile_netto, cash_flow, ricavi, ecc.
    })

    # 3. Composizione finale
    return {
        "anagrafica": anagrafica,
        "bilancio": bilancio,
        "indici": indici,
        "macroarea": macroarea_result["macroarea"],
        "motivazione_macroarea": macroarea_result["motivazione"],
        "note_macroarea": macroarea_result["note"],
        "punteggi_macroarea": macroarea_result["punteggi"],
        "fallback_claude": macroarea_result["fallback_claude"]
    }