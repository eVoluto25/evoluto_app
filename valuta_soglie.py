
def valuta_soglie(indici):
    giudizi = {}

    # MCC semplificato (punteggio 1-4)
    punteggi = []

    # ROE
    roe = indici.get('ROE', 0)
    if roe >= 0.10:
        punteggi.append(1)
    elif roe >= 0.05:
        punteggi.append(2)
    elif roe >= 0:
        punteggi.append(3)
    else:
        punteggi.append(4)

    # EBITDA / Ricavi
    ebitda_ricavi = indici.get('EBITDA/Ricavi', 0)
    if ebitda_ricavi >= 0.15:
        punteggi.append(1)
    elif ebitda_ricavi >= 0.10:
        punteggi.append(2)
    elif ebitda_ricavi >= 0.05:
        punteggi.append(3)
    else:
        punteggi.append(4)

    # PFN / EBITDA
    pfn_ebitda = indici.get('PFN/EBITDA', 0)
    if pfn_ebitda < 2.5:
        punteggi.append(1)
    elif pfn_ebitda < 4:
        punteggi.append(2)
    elif pfn_ebitda < 6:
        punteggi.append(3)
    else:
        punteggi.append(4)

    # PFN / PN
    pfn_pn = indici.get('PFN/PN', 0)
    if pfn_pn < 0.5:
        punteggi.append(1)
    elif pfn_pn < 1:
        punteggi.append(2)
    elif pfn_pn < 2:
        punteggi.append(3)
    else:
        punteggi.append(4)

    # Oneri Fin / Ricavi
    oneri_ricavi = indici.get('Oneri Fin / Ricavi', 0)
    if oneri_ricavi < 0.02:
        punteggi.append(1)
    elif oneri_ricavi < 0.04:
        punteggi.append(2)
    elif oneri_ricavi < 0.07:
        punteggi.append(3)
    else:
        punteggi.append(4)

    # Current Ratio
    current_ratio = indici.get('Current Ratio', 0)
    if current_ratio >= 1.5:
        punteggi.append(1)
    elif current_ratio >= 1.0:
        punteggi.append(2)
    elif current_ratio >= 0.8:
        punteggi.append(3)
    else:
        punteggi.append(4)

    media_punteggio = sum(punteggi) / len(punteggi)

    if media_punteggio <= 1.5:
        classe = "Classe 1 (Ottima)"
    elif media_punteggio <= 2.0:
        classe = "Classe 2 (Buona)"
    elif media_punteggio <= 2.5:
        classe = "Classe 3 (Fragile)"
    elif media_punteggio <= 3.0:
        classe = "Classe 4 (Rischiosa)"
    else:
        classe = "Classe 5 (Critica)"

    giudizi["Classe MCC"] = classe

    # Z-Score
    z = indici.get('Z-Score Altman', 0)
    if z > 2.9:
        giudizi["Z-Score"] = "Sicura"
    elif z > 1.23:
        giudizi["Z-Score"] = "Zona grigia"
    else:
        giudizi["Z-Score"] = "Rischiosa"

    # DSCR
    dscr = indici.get('DSCR', 0)
    if dscr >= 1.5:
        giudizi["DSCR"] = "Solido"
    elif dscr >= 1.0:
        giudizi["DSCR"] = "Tollerabile"
    else:
        giudizi["DSCR"] = "Insostenibile"

    # Leverage
    leverage = indici.get('Leverage', 0)
    if leverage <= 2:
        giudizi["Leverage"] = "Normale"
    elif leverage <= 4:
        giudizi["Leverage"] = "Elevato"
    else:
        giudizi["Leverage"] = "Critico"

    # Indipendenza Finanziaria
    indipendenza = indici.get('Indipendenza Finanziaria', 0)
    if indipendenza >= 0.4:
        giudizi["Indipendenza Finanziaria"] = "Solida"
    elif indipendenza >= 0.25:
        giudizi["Indipendenza Finanziaria"] = "Precaria"
    else:
        giudizi["Indipendenza Finanziaria"] = "Critica"

    # Copertura Immobilizzazioni
    copertura = indici.get('Copertura Immobilizzazioni', 0)
    if copertura >= 1.0:
        giudizi["Copertura Immobilizzazioni"] = "Corretta"
    elif copertura >= 0.8:
        giudizi["Copertura Immobilizzazioni"] = "Parziale"
    else:
        giudizi["Copertura Immobilizzazioni"] = "Sbilanciata"

    return giudizi
