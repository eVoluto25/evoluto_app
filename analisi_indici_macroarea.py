
import logging
from formule_indici import calcola_indici_finanziari

def calcola_indici(dati):
    utile = dati.get("Risultato Netto")
    ricavi = dati.get("Ricavi")
    patrimonio = dati.get("Patrimonio Netto")
    attivo = dati.get("Totale Attivo")
    passivo = dati.get("Totale Passivo")
    liquidita = dati.get("Disponibilità liquide")
    debiti = dati.get("Debiti")
    rimanenze = dati.get("Rimanenze")
    immobilizzazioni = dati.get("Immobilizzazioni")
    oneri_fin = dati.get("Oneri Finanziari")
    ebitda = dati.get("EBITDA")
    ebit = dati.get("EBIT") or ebitda
    attivo_corr = dati.get("Attivo Corrente")
    passivo_corr = dati.get("Passivo Corrente")

    indici = calcola_indici_finanziari({
        "utile_netto": utile,
        "patrimonio_netto": patrimonio,
        "ricavi": ricavi,
        "ebitda": ebitda,
        "debiti_finanziari": debiti,
        "disponibilita": liquidita,
        "totale_attivo": attivo,
        "totale_passivo": passivo,
        "attivo_circolante": attivo_corr,
        "passivo_corrente": passivo_corr,
        "immobilizzazioni": immobilizzazioni,
        "debiti_medio_lungo": dati.get("Debiti M/L Termine", 0),
        "oneri_finanziari": oneri_fin,
        "quota_debito_annua": dati.get("Quota Debito Annua", 0),
        "ebit": ebit,
        "liquidita": liquidita,
        "rimanenze": rimanenze,
        "debiti": debiti
    })

    return indici

def assegna_macro_area(indici):
    try:
        crisi = crescita = espansione = 0

        roe = indici.get("ROE")
        leverage = indici.get("Leverage")
        struttura = indici.get("Margine di Struttura")

        if isinstance(roe, float) and roe < 0.01:
            crisi += 1
        if isinstance(leverage, float) and leverage > 4:
            crisi += 1
        if isinstance(struttura, float) and struttura < 0.8:
            crisi += 1

        if isinstance(roe, float) and roe > 0.05:
            crescita += 1
        if isinstance(struttura, float) and struttura > 1:
            crescita += 1

        if isinstance(roe, float) and roe > 0.1:
            espansione += 1
        if isinstance(leverage, float) and leverage < 2:
            espansione += 1

        logging.info(f"Punteggi: Crisi={crisi}, Crescita={crescita}, Espansione={espansione}")

        if espansione >= 2:
            return "Espansione"
        elif crescita >= 2:
            return "Crescita"
        else:
            return "Crisi"

    except Exception as e:
        logging.error(f"Errore durante l'assegnazione della macro area: {e}")
        return "ND"
