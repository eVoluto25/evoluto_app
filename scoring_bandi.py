import pandas as pd
from config import (
    SCORING_WEIGHTS,
    SCORING_THRESHOLDS,
    PROBABILITY_LABELS
)

def calcola_scoring_bandi(bandi_df, analisi_finanziaria):
    risultati = []
    for _, bando in bandi_df.iterrows():
        punteggio = 0
        max_punteggio = sum(SCORING_WEIGHTS.values())

        if bando['macro_area'] == analisi_finanziaria['macro_area']:
            punteggio += SCORING_WEIGHTS['compatibilita_macro_area']

        if bando['forma_agevolazione'] in SCORING_THRESHOLDS['forma_agevolazione']:
            punteggio += SCORING_WEIGHTS['forma_agevolazione']

        if bando['dimensione_azienda'] == analisi_finanziaria['dimensione_azienda']:
            punteggio += SCORING_WEIGHTS['dimensione_azienda']

        if analisi_finanziaria['indice_solidita'] >= SCORING_THRESHOLDS['indice_solidita']:
            punteggio += SCORING_WEIGHTS['indice_solidita']

        probabilita = (
            PROBABILITY_LABELS['Alta']
            if punteggio >= 0.8 * max_punteggio else
            PROBABILITY_LABELS['Media']
            if punteggio >= 0.5 * max_punteggio else
            PROBABILITY_LABELS['Bassa']
        )

        risultati.append({
            'id_bando': bando['id_bando'],
            'titolo': bando['titolo'],
            'punteggio': punteggio,
            'probabilita_aggiudicazione': probabilita
        })

    # scoring_bandi.py

def simula_beneficio(bando: dict, azienda: dict) -> float:
    try:
        spesa = float(bando.get("spesa_ammessa_min", 0))
        intensita = float(bando.get("intensita_aiuto", 0)) / 100
        beneficio = spesa * intensita
        return beneficio
    except Exception as e:
        print(f"Errore nella simulazione del beneficio: {e}")
        return 0.0

    return pd.DataFrame(risultati)
