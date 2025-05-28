
import pandas as pd

def calcola_scoring(bandi_df, analisi_finanziaria):
    scoring_results = []

    for _, bando in bandi_df.iterrows():
        score = 5  # Punteggio base

        # Esempio di incremento/decremento basato su indici di bilancio
        if analisi_finanziaria['Current Ratio'] >= 1.5:
            score += 1
        elif analisi_finanziaria['Current Ratio'] < 1:
            score -= 2

        if analisi_finanziaria['Debt/Equity'] <= 1:
            score += 1
        elif analisi_finanziaria['Debt/Equity'] > 2:
            score -= 1

        if analisi_finanziaria['EBITDA Margin'] >= 15:
            score += 2
        elif analisi_finanziaria['EBITDA Margin'] < 5:
            score -= 2

        if analisi_finanziaria['Utile netto'] > 0:
            score += 1
        else:
            score -= 1

        # Filtro massimo e minimo
        score = max(1, min(10, score))

        scoring_results.append({
            'ID_Incentivo': bando['ID_Incentivo'],
            'Titolo': bando['Titolo'],
            'Forma_agevolazione': bando['Forma_agevolazione'],
            'Score': score
        })

    return pd.DataFrame(scoring_results)

if __name__ == "__main__":
    bandi_df = pd.read_csv("data/bandi.csv")
    analisi_finanziaria = {
        'Current Ratio': 1.2,
        'Debt/Equity': 1.1,
        'EBITDA Margin': 12,
        'Utile netto': 100000
    }
    risultati = calcola_scoring(bandi_df, analisi_finanziaria)
    risultati.to_csv("data/risultati_scoring.csv", index=False)
