# nomi_standard.py

# Lista completa delle 31 funzioni da importare e usare dinamicamente
FUNZIONI_INDICI = [
    "calcola_roe",
    "calcola_roi",
    "calcola_ros",
    "calcola_roic",
    "calcola_rot",
    "calcola_ebitda_margin",
    "calcola_ebit_oneri_finanziari",
    "calcola_leverage",
    "calcola_debt_equity",
    "calcola_pfn_pn",
    "calcola_indipendenza_finanziaria",
    "calcola_margine_struttura",
    "calcola_copertura_immobilizzazioni",
    "calcola_margine_tesoreria",
    "calcola_capitale_circolante_netto",
    "calcola_quick_ratio",
    "calcola_current_ratio",
    "calcola_mcc",
    "calcola_dscr",
    "calcola_cashflow_debiti",
    "calcola_liquidita_immediata",
    "calcola_acid_test",
    "calcola_coverage_ratio",
    "calcola_cf_operativo_ricavi",
    "calcola_cf_operativo_attivo",
    "calcola_attivita_correnti_su_attivo",
    "calcola_oneri_ricavi",
    "calcola_roa",
    "calcola_capitale_netto_attivo",
    "calcola_rigidita_investimenti",
    "calcola_autonomia_finanziaria"
]

# Mappatura funzione indice → macroarea (per assegnazione punteggio)
INDICE_TO_MACROAREA = {
    "calcola_current_ratio": "crisi",
    "calcola_debt_equity": "crisi",
    "calcola_ebit_oneri_finanziari": "crisi",
    "calcola_ebitda_margin": "crisi",
    "calcola_roa": "crisi",
    "calcola_cf_operativo_attivo": "crescita",
    "calcola_indipendenza_finanziaria": "crescita",
    "calcola_rigidita_investimenti": "crescita",
    "calcola_ros": "espansione",
    "calcola_ebitda_margin": "espansione",
    "fatturato_crescente": "espansione"
}

# Soglie di riferimento (intervalli o valori minimi)
SOGLIE_INDICI = {
    "calcola_current_ratio": 1.0,
    "calcola_debt_equity": (0.5, 2.0),
    "calcola_ebit_oneri_finanziari": 1.0,
    "calcola_ebitda_margin": 0.0,
    "calcola_roa": 0.0,
    "calcola_cf_operativo_attivo": 0.0,
    "calcola_indipendenza_finanziaria": 0.3,
    "calcola_rigidita_investimenti": 0.2,
    "calcola_ros": 0.05,
    "fatturato_crescente": True
}

# Punteggi associati a soglie
PUNTEGGI_INDICI = {
    "superata": 1,
    "borderline": 0.5,
    "mancante": 0,
    "critica": -1,
    "fuori_soglia": -5
}