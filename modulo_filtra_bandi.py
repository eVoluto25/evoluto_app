import logging
import pandas as pd
import ast
from rapidfuzz import fuzz

logger = logging.getLogger(__name__)

MCC_RATING_PUNTEGGIO = {
    "AAA": 10,
    "AA": 9,
    "A": 8,
    "BBB": 7,
    "BB": 6,
    "B": 4,
    "CCC": 2
}

Z_SCORE_PUNTEGGIO = [
    (-9999, 0, 2),
    (0, 1.8, 4),
    (1.8, 2.99, 7),
    (3, 9999, 10)
]

def punteggio_zscore(z_score: float) -> int:
    for min_val, max_val, score in Z_SCORE_PUNTEGGIO:
        if min_val <= z_score <= max_val:
            return score
    return 5

def livello_coerenza_solidita(punteggio: float) -> str:
    if punteggio >= 9:
        return "Eccellente 🟢"
    elif punteggio >= 7:
        return "Alta 🟢"
    elif punteggio >= 5:
        return "Media 🟡"
    elif punteggio >= 3:
        return "Bassa 🟠"
    else:
        return "Critica 🔴"

def semaforo_punteggio(punteggio: float) -> str:
    if punteggio >= 13:
        return "🟢 Ottimo"
    elif punteggio >= 10:
        return "🟡 Buono"
    elif punteggio >= 7:
        return "🟠 Medio"
    else:
        return "🔴 Basso"

def semaforo_priorita(priorita: int) -> str:
    if priorita == 1:
        return "🟢 Alta coerenza"
    return "🟡 Coerenza parziale"

def motivazione_solidita(punteggio: float) -> str:
    if punteggio >= 9:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda presenta una solidità ECCELLENTE. "
            "Il bando è pienamente coerente con la struttura economico-finanziaria e rappresenta un'opportunità prioritaria di sviluppo. 🟢"
        )
    elif punteggio >= 7:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda mostra una solidità ALTA. "
            "Il bando è coerente con le performance aziendali e può supportare investimenti strategici. 🟢"
        )
    elif punteggio >= 5:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda possiede una solidità MEDIA. "
            "La partecipazione al bando è possibile, ma si consiglia un'attenta valutazione della capacità di cofinanziamento. 🟡"
        )
    elif punteggio >= 3:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda evidenzia una solidità BASSA. "
            "Il bando potrebbe presentare criticità in fase di candidatura, si raccomanda cautela. 🟠"
        )
    else:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda mostra una solidità CRITICA. "
            "Il bando selezionato non è consigliato senza interventi di miglioramento della situazione finanziaria. 🔴"
        )

def riassunto_50_parole(testo):
    if not testo:
        return ""
    parole = testo.split()
    if len(parole) <= 50:
        return testo
    return " ".join(parole[:50]) + "..."

def parse_list_field(x):
    if pd.isna(x):
        return []
    try:
        return ast.literal_eval(x)
    except Exception:
        return []

def obiettivo_simile(lista_obiettivi, target):
    """
    Verifica se un obiettivo della lista è simile al target (fuzzy match >=80).
    """
    return any(fuzz.partial_ratio(o.lower(), target.lower()) >= 80 for o in lista_obiettivi)

def punteggio_forma_agevolazione(forma):
    """
    Punteggio aggiuntivo per la forma dell'agevolazione.
    Fondo perduto: 3
    Fondo + prestito: 2
    Solo prestito: 1
    """
    if not forma:
        return 1
    forma = forma.lower()
    if "fondo perduto" in forma:
        return 3
    if "prestito" in forma and "fondo" in forma:
        return 2
    if "prestito" in forma:
        return 1
    return 1

def punteggio_scadenza(data):
    """
    Priorità in base alla scadenza.
    >=180 giorni: 3
    90-179 giorni: 2
    <90 giorni: 1
    """
    if pd.isna(data):
        return 3
    giorni = (data - pd.Timestamp.today()).days
    if giorni >= 180:
        return 3
    elif giorni >= 90:
        return 2
    else:
        return 1

def filtra_bandi(
    df: pd.DataFrame,
    regione: str,
    dimensione: str,
    obiettivo_preferenziale: str,
    mcc_rating: str,
    z_score: float,
    max_results: int = 50
) -> list:
    logger.info(">>> Filtro regione: %s", regione)
    logger.info(">>> Filtro dimensione: %s", dimensione)
    logger.info(">>> Obiettivo preferenziale: %s", obiettivo_preferenziale)
    logger.info(">>> MCC: %s | Z-Score: %s", mcc_rating, z_score)

    # Parsing liste
    df["dimensioni_list"] = df["Dimensioni"].apply(parse_list_field)
    df["regioni_list"] = df["Regioni"].apply(parse_list_field)
    df["obiettivo_list"] = df["Obiettivo_Finalita"].apply(parse_list_field)

    # Pulizia stringhe
    df["titolo_clean"] = df["Titolo"].astype(str).str.strip()
    df["descrizione_clean"] = df["Descrizione"].astype(str).str.strip()
    df["forma_agevolazione_clean"] = df["Forma_Agevolazione"].astype(str).str.strip()

    obiettivo_clean = obiettivo_preferenziale.strip()
    dimensione_clean = dimensione.strip()
    regione_clean = regione.strip()

    # Punteggio solidità
    mcc_punteggio = MCC_RATING_PUNTEGGIO.get(mcc_rating.upper(), 5)
    z_punteggio = punteggio_zscore(z_score)
    media_punteggio = (mcc_punteggio + z_punteggio) / 2

    solidita_critica = (
        mcc_rating.upper() in ["CCC", "B"]
        and z_score <= 0
    )
    if solidita_critica:
        logger.info(">>> Solidità critica: filtreremo solo bandi di sostegno.")
    else:
        logger.info(">>> Solidità non critica.")

    # Filtro scadenza
    oggi = pd.Timestamp.today()
    df["Data_chiusura_parsed"] = pd.to_datetime(df["data_chiusura_clean"], errors="coerce")
    scadenza_limite = oggi + pd.Timedelta(days=45)
    df = df[
        (df["Data_chiusura_parsed"].isna())
        | (df["Data_chiusura_parsed"] >= scadenza_limite)
    ]
    if df.empty:
        logger.info(">>> Nessun bando con scadenza oltre 45 giorni.")
        return []

    def match_regione(l, regione):
        if not l:
            return False
        return (regione in l) or ("tutte le regioni" in [s.lower() for s in l])

    if solidita_critica:
        df_selected = df[
            df["regioni_list"].apply(lambda l: match_regione(l, regione_clean))
            &
            df["obiettivo_list"].apply(lambda l: any("sostegno" in s.lower() for s in l))
            &
            df["dimensioni_list"].apply(lambda l: dimensione_clean in l)
        ]
    else:
        df_step1 = df[
            df["regioni_list"].apply(lambda l: match_regione(l, regione_clean))
            &
            df["obiettivo_list"].apply(lambda l: obiettivo_simile(l, obiettivo_clean))
            &
            df["dimensioni_list"].apply(lambda l: dimensione_clean in l)
        ]
        if not df_step1.empty:
            df_selected = df_step1.copy()
        else:
            df_step2 = df[
                df["regioni_list"].apply(lambda l: match_regione(l, regione_clean))
                &
                df["dimensioni_list"].apply(lambda l: dimensione_clean in l)
            ]
            if not df_step2.empty:
                df_selected = df_step2.copy()
            else:
                df_selected = df[
                    df["dimensioni_list"].apply(lambda l: dimensione_clean in l)
                ]

    if df_selected.empty:
        return []

    # Priorità obiettivo
    df_selected["Priorita_Obiettivo"] = df_selected["obiettivo_list"].apply(
        lambda l: 1 if obiettivo_simile(l, obiettivo_clean) else 2
    )
    # Punteggio forma agevolazione
    df_selected["Punteggio_Forma"] = df_selected["forma_agevolazione_clean"].apply(punteggio_forma_agevolazione)
    # Punteggio scadenza
    df_selected["Punteggio_Scadenza"] = df_selected["Data_chiusura_parsed"].apply(punteggio_scadenza)
    # Punteggio totale
    df_selected["Punteggio_Totale"] = media_punteggio + df_selected["Punteggio_Forma"] + df_selected["Punteggio_Scadenza"]

    df_sorted = df_selected.sort_values(
        by=["Priorita_Obiettivo", "Punteggio_Totale", "Data_chiusura_parsed"],
        ascending=[True, False, True]
    ).head(max_results)

    risultati = []
    for _, row in df_sorted.iterrows():
        descrizione_ridotta = riassunto_50_parole(row.get("descrizione_clean", ""))
        data_chiusura = row.get("data_chiusura_clean", "")
        if not data_chiusura or str(data_chiusura).strip() == "":
            data_chiusura = "bando disponibile fino ad esaurimento fondi. Verificare residuo stanziamento."
        risultati.append({
            "titolo": row.get("titolo_clean", ""),
            "data": data_chiusura,
            "coerenza_solidita": livello_coerenza_solidita(media_punteggio),
            "obiettivo_finalita": row.get("obiettivo_list", []),
            "punteggio_totale": row.get("Punteggio_Totale", 0),
            "semaforo_punteggio_totale": semaforo_punteggio(row.get("Punteggio_Totale", 0)),
            "priorita_obiettivo": row.get("Priorita_Obiettivo", 2),
            "semaforo_priorita_obiettivo": semaforo_priorita(row.get("Priorita_Obiettivo", 2)),
            "percentuale_ammissibilità": row.get("percentuale_ammissibilità", ""),
            "motivazione": motivazione_solidita(media_punteggio),
            "forma_agevolazione": row.get("forma_agevolazione_clean", ""),
            "costi_ammessi": row.get("Costi_Ammessi", ""),
            "descrizione": descrizione_ridotta
        })

    return risultati
