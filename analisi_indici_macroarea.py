# analisi_indici_macroarea.py

import logging
from formule_indici import *
from nomi_standard import FUNZIONI_INDICI, INDICE_TO_MACROAREA, SOGLIE_INDICI, PUNTEGGI_INDICI

logging.basicConfig(level=logging.INFO)

def valuta_indice(nome_funzione, valore):
    soglia = SOGLIE_INDICI.get(nome_funzione)
    if valore is None:
        return PUNTEGGI_INDICI["mancante"]
    if isinstance(soglia, tuple):
        if soglia[0] <= valore <= soglia[1]:
            return PUNTEGGI_INDICI["superata"]
        return PUNTEGGI_INDICI["critica"]
    if isinstance(soglia, (int, float)):
        if valore > soglia:
            return PUNTEGGI_INDICI["superata"]
        if valore == soglia:
            return PUNTEGGI_INDICI["borderline"]
        return PUNTEGGI_INDICI["critica"]
    return 0

def analizza_macroarea(dati):
    indici = {}
    punteggi = {"crisi": 0, "crescita": 0, "espansione": 0}
    log_warning = []
    dati_incompleti = False

    for nome_funzione in FUNZIONI_INDICI:
        if nome_funzione not in INDICE_TO_MACROAREA:
            continue
        try:
            funzione = globals()[nome_funzione]
            args = funzione.__code__.co_varnames[:funzione.__code__.co_argcount]
            input_args = [dati.get(a) for a in args]
            valore = funzione(*input_args)
            indici[nome_funzione] = valore
            macroarea = INDICE_TO_MACROAREA[nome_funzione]
            score = valuta_indice(nome_funzione, valore)
            punteggi[macroarea] += score
            if valore is None:
                dati_incompleti = True
                log_warning.append(f"{nome_funzione} → ND (dati mancanti)")
        except Exception as e:
            log_warning.append(f"{nome_funzione} → Errore: {str(e)}")
            dati_incompleti = True

    macroarea_primaria = max(punteggi, key=punteggi.get)
    punteggi_values = list(punteggi.values())
    macroarea_alternativa = None
    if punteggi_values.count(punteggi[macroarea_primaria]) > 1:
        macroarea_alternativa = "parità"
        dati_incompleti = True

    return {
        "macroarea_primaria": macroarea_primaria.upper(),
        "macroarea_alternativa": macroarea_alternativa,
        "macroarea_validata_claude": None,
        "indici": indici,
        "punteggi_macroaree": punteggi,
        "dati_incompleti": dati_incompleti,
        "log_warning": log_warning
    }