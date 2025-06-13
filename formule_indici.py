def calcola_roe(utile_netto, patrimonio_netto):
    try:
        return utile_netto / patrimonio_netto if patrimonio_netto else 0
    except Exception:
        return 0

def calcola_roi(ebit, totale_attivo):
    try:
        return ebit / totale_attivo if totale_attivo else 0
    except Exception:
        return 0

def calcola_ros(ebit, ricavi):
    try:
        return ebit / ricavi if ricavi else 0
    except Exception:
        return 0

def calcola_roic(ebit, capitale_investito):
    try:
        return ebit / capitale_investito if capitale_investito else 0
    except Exception:
        return 0

def calcola_rot(ricavi, totale_attivo):
    try:
        return ricavi / totale_attivo if totale_attivo else 0
    except Exception:
        return 0

def calcola_ebitda_margin(ebitda, ricavi):
    try:
        return ebitda / ricavi if ricavi else 0
    except Exception:
        return 0

def calcola_ebit_of(ebit, oneri_fin):
    try:
        return ebit / oneri_fin if oneri_fin else 0
    except Exception:
        return 0

def calcola_leverage(totale_passivo, patrimonio_netto):
    try:
        return totale_passivo / patrimonio_netto if patrimonio_netto else 0
    except Exception:
        return 0

def calcola_debt_equity(debiti, patrimonio_netto):
    try:
        return debiti / patrimonio_netto if patrimonio_netto else 0
    except Exception:
        return 0

def calcola_pfnpn(pfn, patrimonio_netto):
    try:
        return pfn / patrimonio_netto if patrimonio_netto else 0
    except Exception:
        return 0

def calcola_indipendenza_fin(patrimonio_netto, totale_fonti):
    try:
        return patrimonio_netto / totale_fonti if totale_fonti else 0
    except Exception:
        return 0

def calcola_margine_struttura(patrimonio_netto, immobilizzazioni):
    try:
        return patrimonio_netto / immobilizzazioni if immobilizzazioni else 0
    except Exception:
        return 0

def calcola_copertura_imm(cap_medio_termine, immobilizzazioni):
    try:
        return cap_medio_termine / immobilizzazioni if immobilizzazioni else 0
    except Exception:
        return 0

def calcola_margine_tesoreria(liquidita_imm, debiti_brevedurata):
    try:
        return liquidita_imm / debiti_brevedurata if debiti_brevedurata else 0
    except Exception:
        return 0

def calcola_ccn(attivo_corr, passivo_corr):
    try:
        return attivo_corr / passivo_corr if passivo_corr else 0
    except Exception:
        return 0

def calcola_quick_ratio(liquidita_imm, passivo_corr):
    try:
        return liquidita_imm / passivo_corr if passivo_corr else 0
    except Exception:
        return 0

def calcola_current_ratio(attivo_corr, passivo_corr):
    try:
        return attivo_corr / passivo_corr if passivo_corr else 0
    except Exception:
        return 0

def calcola_mcc(attivo_corr, passivo_corr):
    try:
        return attivo_corr / passivo_corr if passivo_corr else 0
    except Exception:
        return 0

def calcola_dscr(cash_flow_operativo, quota_debiti):
    try:
        return cash_flow_operativo / quota_debiti if quota_debiti else 0
    except Exception:
        return 0

def calcola_cashflow_debiti(cash_flow_operativo, debiti):
    try:
        return cash_flow_operativo / debiti if debiti else 0
    except Exception:
        return 0

def calcola_liquidita_immediata(disponibilita, passivo_corr):
    try:
        return disponibilita / passivo_corr if passivo_corr else 0
    except Exception:
        return 0

def calcola_acid_test(liquidita_imm, passivo_corr):
    try:
        return liquidita_imm / passivo_corr if passivo_corr else 0
    except Exception:
        return 0

def calcola_coverage_ratio(ebitda, oneri_fin):
    try:
        return ebitda / oneri_fin if oneri_fin else 0
    except Exception:
        return 0

def calcola_cf_ricavi(cash_flow_operativo, ricavi):
    try:
        return cash_flow_operativo / ricavi if ricavi else 0
    except Exception:
        return 0

def calcola_cf_attivo(cash_flow_operativo, totale_attivo):
    try:
        return cash_flow_operativo / totale_attivo if totale_attivo else 0
    except Exception:
        return 0

def calcola_att_corr_attivo(attivo_corr, totale_attivo):
    try:
        return attivo_corr / totale_attivo if totale_attivo else 0
    except Exception:
        return 0

def calcola_oneri_ricavi(oneri_fin, ricavi):
    try:
        return oneri_fin / ricavi if ricavi else 0
    except Exception:
        return 0

def calcola_roa(utile_netto, totale_attivo):
    try:
        return utile_netto / totale_attivo if totale_attivo else 0
    except Exception:
        return 0

def calcola_cap_netto_attivo(capitale_netto, totale_attivo):
    try:
        return capitale_netto / totale_attivo if totale_attivo else 0
    except Exception:
        return 0

def calcola_rigidita_inv(immobilizzazioni, totale_attivo):
    try:
        return immobilizzazioni / totale_attivo if totale_attivo else 0
    except Exception:
        return 0

def calcola_autonomia_finanziaria(patrimonio_netto, totale_passivo):
    try:
        return patrimonio_netto / totale_passivo if totale_passivo else 0
    except Exception:
        return 0
