
import pandas as pd

def calcola_punteggio(row):
    punteggio = 0

    # Peso per compatibilità macro area
    if row['compatibilita_macro_area']:
        punteggio += 30

    # Peso per forma agevolazione
    if row['forma_agevolazione'] in ['fondo perduto', 'credito d’imposta']:
        punteggio += 25
    elif row['forma_agevolazione'] in ['finanziamento agevolato', 'tasso zero']:
        punteggio += 15

    # Peso per dimensioni azienda
    if row['dimensione_azienda'] == 'PMI':
        punteggio += 20
    elif row['dimensione_azienda'] == 'micro':
        punteggio += 10

    # Peso per settorialità (compatibilità con codice ATECO)
    if row['settore_compatibile']:
        punteggio += 15

    # Peso per copertura geografica
    if row['copertura_territoriale'] == 'regionale':
        punteggio += 5
    elif row['copertura_territoriale'] == 'nazionale':
        punteggio += 10

    return punteggio

def classifica_probabilita(punteggio):
    if punteggio >= 80:
        return 'Alta'
    elif 50 <= punteggio < 80:
        return 'Media'
    else:
        return 'Bassa'

def applica_scoring(df):
    df['punteggio'] = df.apply(calcola_punteggio, axis=1)
    df['classificazione_probabilita'] = df['punteggio'].apply(classifica_probabilita)
    return df
