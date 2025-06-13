
from formule_indici import calcola_indici_finanziari

indici = calcola_indici_finanziari({
    "utile_netto": dati.get("Risultato Netto", 0),
    "patrimonio_netto": dati.get("Patrimonio Netto", 0),
    "ricavi": dati.get("Ricavi", 0),
    "ebitda": dati.get("EBITDA", 0),
    "debiti_finanziari": dati.get("Debiti", 0),
    "disponibilita": dati.get("Disponibilità liquide", 0),
    "totale_attivo": dati.get("Totale Attivo", 0),
    "totale_passivo": dati.get("Totale Passivo", 0),
    "attivo_circolante": dati.get("Attivo Corrente", 0),
    "passivo_corrente": dati.get("Passivo Corrente", 0),
    "immobilizzazioni": dati.get("Immobilizzazioni", 0),
    "debiti_medio_lungo": dati.get("Debiti M/L Termine", 0),
    "oneri_finanziari": dati.get("Oneri Finanziari", 0),
    "quota_debito_annua": dati.get("Quota Debito Annua", 0)
})

    # MCC semplificato
    risultati['ROE'] = utile_netto / patrimonio_netto if patrimonio_netto != 0 else 0
    risultati['EBITDA/Ricavi'] = ebitda / ricavi if ricavi != 0 else 0
    risultati['PFN/EBITDA'] = pfnet / ebitda if ebitda != 0 else 0
    risultati['PFN/PN'] = pfnet / patrimonio_netto if patrimonio_netto != 0 else 0
    risultati['Oneri Fin / Ricavi'] = oneri_finanziari / ricavi if ricavi != 0 else 0
    risultati['Current Ratio'] = attivo_circolante / passivo_corrente if passivo_corrente != 0 else 0

    # Z-Score Altman (semplificato per PMI)
    try:
        risultati['Z-Score Altman'] = (
            0.717 * (ebitda / totale_attivo) +
            0.847 * (patrimonio_netto / totale_passivo) +
            3.107 * (utile_netto / totale_attivo) +
            0.420 * ((attivo_circolante - passivo_corrente) / totale_attivo) +
            0.998 * (ricavi / totale_attivo)
        )
    except ZeroDivisionError:
        risultati['Z-Score Altman'] = 0

    # DSCR
    risultati['DSCR'] = ebitda / quota_debito_annua if quota_debito_annua != 0 else 0

    # Leverage
    risultati['Leverage'] = totale_attivo / patrimonio_netto if patrimonio_netto != 0 else 0

    # Indipendenza Finanziaria
    risultati['Indipendenza Finanziaria'] = patrimonio_netto / totale_passivo if totale_passivo != 0 else 0

    # Copertura Immobilizzazioni
    risultati['Copertura Immobilizzazioni'] = (patrimonio_netto + debiti_medio_lungo) / immobilizzazioni if immobilizzazioni != 0 else 0

    return risultati
