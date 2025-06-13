def calcola_roe(utile_netto, patrimonio_netto):
    if utile_netto is None or patrimonio_netto in (None, 0):
        return "ND"
    return round(utile_netto / patrimonio_netto, 6)

def calcola_debt_equity(debiti, patrimonio):
    try:
        return debiti / patrimonio if patrimonio else 0
    except Exception:
        return 0

def calcola_ebitda_margin(ebitda, ricavi):
    try:
        return ebitda / ricavi if ricavi else 0
    except Exception:
        return 0

def calcola_interest_coverage(ebitda, oneri_fin):
    try:
        return ebitda / oneri_fin if oneri_fin else 0
    except Exception:
        return 0

def calcola_roi(ebit, totale_attivo):
    if ebit is None or totale_attivo in (None, 0):
        return "ND"
    return round(ebit / totale_attivo, 6)

def calcola_ros(ebit, ricavi):
    if ebit is None or ricavi in (None, 0):
        return "ND"
    return round(ebit / ricavi, 6)

def calcola_roic(ebit, debiti, patrimonio_netto):
    capitale_investito = (debiti or 0) + (patrimonio_netto or 0)
    if ebit is None or capitale_investito in (None, 0):
        return "ND"
    return round(ebit / capitale_investito, 6)

def calcola_rot(ricavi, totale_attivo):
    if ricavi is None or totale_attivo in (None, 0):
        return "ND"
    return round(ricavi / totale_attivo, 6)

def calcola_leverage(totale_passivo, patrimonio_netto):
    if totale_passivo is None or patrimonio_netto in (None, 0):
        return "ND"
    return round(totale_passivo / patrimonio_netto, 6)

def calcola_pfnpn(debiti_totali, liquidita, patrimonio_netto):
    pfn = (debiti_totali or 0) - (liquidita or 0)
    if patrimonio_netto in (None, 0):
        return "ND"
    return round(pfn / patrimonio_netto, 6)

def calcola_ebit_of(ebit, oneri_finanziari):
    if ebit is None or oneri_finanziari in (None, 0):
        return "ND"
    return round(ebit / oneri_finanziari, 6)

def calcola_current_ratio(attivo_corrente, passivo_corrente):
    if attivo_corrente is None or passivo_corrente in (None, 0):
        return "ND"
    return round(attivo_corrente / passivo_corrente, 6)

def calcola_quick_ratio(attivo_corrente, rimanenze, passivo_corrente):
    if attivo_corrente is None or passivo_corrente in (None, 0):
        return "ND"
    return round((attivo_corrente - (rimanenze or 0)) / passivo_corrente, 6)

def calcola_indipendenza_fin(patrimonio_netto, totale_attivo):
    if patrimonio_netto is None or totale_attivo in (None, 0):
        return "ND"
    return round(patrimonio_netto / totale_attivo, 6)

def calcola_margine_tesoreria(liquidita, passivo_corrente):
    if liquidita is None or passivo_corrente in (None, 0):
        return "ND"
    return round(liquidita / passivo_corrente, 6)

def calcola_copertura_imm(patrimonio_netto, immobilizzazioni):
    if patrimonio_netto is None or immobilizzazioni in (None, 0):
        return "ND"
    return round(patrimonio_netto / immobilizzazioni, 6)

def calcola_margine_struttura(patrimonio_netto, immobilizzazioni):
    return calcola_copertura_imm(patrimonio_netto, immobilizzazioni)

def calcola_ccn(attivo_corrente, passivo_corrente):
    if attivo_corrente is None or passivo_corrente is None:
        return "ND"
    return round(attivo_corrente - passivo_corrente, 2)
