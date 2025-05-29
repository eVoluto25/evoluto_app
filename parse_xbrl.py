
"""
Modulo per il parsing centralizzato dei documenti aziendali.
Combina l'estrazione dei dati finanziari da XBRL e anagrafici dalla visura PDF.
"""

from extractor import estrai_dati_bilancio, estrai_anagrafica_visura

def parse_xbrl(uploaded_xbrl, uploaded_visura):
    """
    Estrae i dati di bilancio (da file XBRL) e i dati anagrafici (da PDF della visura camerale).

    Args:
        uploaded_xbrl: file XBRL caricato dall'utente.
        uploaded_visura: file PDF della visura camerale.

    Returns:
        tuple: (dati_bilancio, anagrafica)
    """
    dati_bilancio = estrai_dati_bilancio(uploaded_xbrl)
    anagrafica = estrai_anagrafica_visura(uploaded_visura)
    return dati_bilancio, anagrafica
