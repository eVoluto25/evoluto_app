
def calcola_indici_finanziari(dati):
    risultati = {}

    utile_netto = dati.get("utile_netto", 0)
    patrimonio_netto = dati.get("patrimonio_netto", 0)
    ricavi = dati.get("ricavi", 0)
    ebitda = dati.get("ebitda", 0)
    debiti_finanziari = dati.get("debiti_finanziari", 0)
    disponibilita = dati.get("disponibilita", 0)
    totale_attivo = dati.get("totale_attivo", 0)
    totale_passivo = dati.get("totale_passivo", 0)
    attivo_circolante = dati.get("attivo_circolante", 0)
    passivo_corrente = dati.get("passivo_corrente", 0)
    immobilizzazioni = dati.get("immobilizzazioni", 0)
    debiti_medio_lungo = dati.get("debiti_medio_lungo", 0)
    oneri_finanziari = dati.get("oneri_finanziari", 0)
    quota_debito_annua = dati.get("quota_debito_annua", 0)

    pfnet = debiti_finanziari - disponibilita

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
