# formule_indici.py

def calcola_roe(utile_netto, patrimonio_netto):
    if utile_netto is None or patrimonio_netto in (None, 0):
        return None
    return utile_netto / patrimonio_netto

def calcola_roi(ebit, totale_attivo):
    if ebit is None or totale_attivo in (None, 0):
        return None
    return ebit / totale_attivo

def calcola_ros(ebit, ricavi):
    if ebit is None or ricavi in (None, 0):
        return None
    return ebit / ricavi

def calcola_roic(ebit, capitale_netto_attivo):
    if ebit is None or capitale_netto_attivo in (None, 0):
        return None
    return ebit / capitale_netto_attivo

def calcola_rot(ricavi, capitale_netto_attivo):
    if ricavi is None or capitale_netto_attivo in (None, 0):
        return None
    return ricavi / capitale_netto_attivo

def calcola_ebitda_margin(ebitda, ricavi):
    if ebitda is None or ricavi in (None, 0):
        return None
    return ebitda / ricavi

def calcola_ebit_oneri_finanziari(ebit, oneri_finanziari):
    if ebit is None or oneri_finanziari in (None, 0):
        return None
    return ebit / oneri_finanziari

def calcola_leverage(totale_attivo, patrimonio_netto):
    if totale_attivo is None or patrimonio_netto in (None, 0):
        return None
    return totale_attivo / patrimonio_netto

def calcola_debt_equity(totale_debiti, patrimonio_netto):
    if totale_debiti is None or patrimonio_netto in (None, 0):
        return None
    return totale_debiti / patrimonio_netto

def calcola_pfn_pn(pfn, patrimonio_netto):
    if pfn is None or patrimonio_netto in (None, 0):
        return None
    return pfn / patrimonio_netto

def calcola_indipendenza_finanziaria(patrimonio_netto, totale_passivo):
    if patrimonio_netto is None or totale_passivo in (None, 0):
        return None
    return patrimonio_netto / totale_passivo

def calcola_margine_struttura(patrimonio_netto, immobilizzazioni):
    if patrimonio_netto is None or immobilizzazioni is None:
        return None
    return patrimonio_netto - immobilizzazioni

def calcola_copertura_immobilizzazioni(patrimonio_netto, passivo_consolidato, immobilizzazioni):
    if None in (patrimonio_netto, passivo_consolidato, immobilizzazioni) or immobilizzazioni == 0:
        return None
    return (patrimonio_netto + passivo_consolidato) / immobilizzazioni

def calcola_margine_tesoreria(liquidita, crediti, debiti_brevi):
    if None in (liquidita, crediti, debiti_brevi):
        return None
    return liquidita + crediti - debiti_brevi

def calcola_capitale_circolante_netto(attivo_corrente, passivo_corrente):
    if attivo_corrente is None or passivo_corrente is None:
        return None
    return attivo_corrente - passivo_corrente

def calcola_quick_ratio(liquidita, crediti, passivo_corrente):
    if None in (liquidita, crediti, passivo_corrente) or passivo_corrente == 0:
        return None
    return (liquidita + crediti) / passivo_corrente

def calcola_current_ratio(attivo_corrente, passivo_corrente):
    if None in (attivo_corrente, passivo_corrente) or passivo_corrente == 0:
        return None
    return attivo_corrente / passivo_corrente

def calcola_mcc(cassa, debiti_brevi):
    if cassa is None or debiti_brevi in (None, 0):
        return None
    return cassa / debiti_brevi

def calcola_dscr(cash_flow_operativo, quota_debiti_finanziari):
    if cash_flow_operativo is None or quota_debiti_finanziari in (None, 0):
        return None
    return cash_flow_operativo / quota_debiti_finanziari

def calcola_cashflow_debiti(cash_flow_operativo, debiti_finanziari):
    if None in (cash_flow_operativo, debiti_finanziari) or debiti_finanziari == 0:
        return None
    return cash_flow_operativo / debiti_finanziari

def calcola_liquidita_immediata(liquidita, passivo_corrente):
    if None in (liquidita, passivo_corrente) or passivo_corrente == 0:
        return None
    return liquidita / passivo_corrente

def calcola_acid_test(liquidita, crediti_brevi, rimanenze, passivo_corrente):
    if None in (liquidita, crediti_brevi, rimanenze, passivo_corrente) or passivo_corrente == 0:
        return None
    return (liquidita + crediti_brevi - rimanenze) / passivo_corrente

def calcola_coverage_ratio(interessi_attivi, oneri_finanziari):
    if interessi_attivi is None or oneri_finanziari in (None, 0):
        return None
    return interessi_attivi / oneri_finanziari

def calcola_cf_operativo_ricavi(cash_flow_operativo, ricavi):
    if None in (cash_flow_operativo, ricavi) or ricavi == 0:
        return None
    return cash_flow_operativo / ricavi

def calcola_cf_operativo_attivo(cash_flow_operativo, attivo_totale):
    if None in (cash_flow_operativo, attivo_totale) or attivo_totale == 0:
        return None
    return cash_flow_operativo / attivo_totale

def calcola_attivita_correnti_su_attivo(attivo_corrente, attivo_totale):
    if None in (attivo_corrente, attivo_totale) or attivo_totale == 0:
        return None
    return attivo_corrente / attivo_totale

def calcola_oneri_ricavi(oneri_finanziari, ricavi):
    if None in (oneri_finanziari, ricavi) or ricavi == 0:
        return None
    return oneri_finanziari / ricavi

def calcola_roa(utile_netto, totale_attivo):
    if None in (utile_netto, totale_attivo) or totale_attivo == 0:
        return None
    return utile_netto / totale_attivo

def calcola_capitale_netto_attivo(patrimonio_netto, passivo_consolidato):
    if None in (patrimonio_netto, passivo_consolidato):
        return None
    return patrimonio_netto + passivo_consolidato

def calcola_rigidita_investimenti(immobilizzazioni, attivo_totale):
    if None in (immobilizzazioni, attivo_totale) or attivo_totale == 0:
        return None
    return immobilizzazioni / attivo_totale

def calcola_autonomia_finanziaria(patrimonio_netto, totale_fonti):
    if None in (patrimonio_netto, totale_fonti) or totale_fonti == 0:
        return None
    return patrimonio_netto / totale_fonti
