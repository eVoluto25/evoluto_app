
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
    ebit = dati.get("ebit", ebitda)
    debiti = dati.get("debiti", 0)
    liquidita = dati.get("liquidita", 0)
    rimanenze = dati.get("rimanenze", 0)

    pfnet = debiti_finanziari - disponibilita

    # MCC semplificato
    risultati['ROE'] = utile_netto / patrimonio_netto if patrimonio_netto != 0 else 0
    risultati['EBITDA/Ricavi'] = ebitda / ricavi if ricavi != 0 else 0
    risultati['PFN/EBITDA'] = pfnet / ebitda if ebitda != 0 else 0
    risultati['PFN/PN'] = pfnet / patrimonio_netto if patrimonio_netto != 0 else 0
    risultati['Oneri Fin / Ricavi'] = oneri_finanziari / ricavi if ricavi != 0 else 0
    risultati['Current Ratio'] = attivo_circolante / passivo_corrente if passivo_corrente != 0 else 0

    # Z-Score Altman
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
    risultati['Copertura Immobilizzazioni'] = (
        (patrimonio_netto + debiti_medio_lungo) / immobilizzazioni
        if immobilizzazioni != 0 else 0
    )

    # Altri indici estesi
    risultati['ROI'] = ebit / totale_attivo if totale_attivo != 0 else 0
    risultati['ROS'] = ebit / ricavi if ricavi != 0 else 0
    risultati['ROIC'] = ebit / (debiti + patrimonio_netto) if (debiti + patrimonio_netto) != 0 else 0
    risultati['ROT'] = ricavi / totale_attivo if totale_attivo != 0 else 0
    risultati['EBIT/OF'] = ebit / oneri_finanziari if oneri_finanziari != 0 else 0
    risultati['Quick Ratio'] = (attivo_circolante - rimanenze) / passivo_corrente if passivo_corrente != 0 else 0
    risultati['Margine di Tesoreria'] = liquidita - passivo_corrente
    risultati['Margine di Struttura'] = patrimonio_netto - immobilizzazioni
    risultati['Capitale Circolante Netto'] = attivo_circolante - passivo_corrente
    risultati['Debt/Equity'] = debiti / patrimonio_netto if patrimonio_netto != 0 else 0
    risultati['EBITDA Margin'] = ebitda / ricavi if ricavi != 0 else 0
    risultati['Interest Coverage'] = ebitda / oneri_finanziari if oneri_finanziari != 0 else 0

    return risultati
