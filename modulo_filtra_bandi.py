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

def motivazione_solidita(punteggio: float) -> str:
    if punteggio >= 9:
        return (
            "Secondo l'analisi del sistema eVoluto, l'azienda presenta una solidità ECCELLENTE. "
            "Il bando è pienamente coerente con la struttura economico-finanziaria e rappresenta un'opportunità prioritaria di sviluppo. 🔵"
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

def riassunto_30_parole(testo):
    if not testo:
        return ""
    parole = testo.split()
    if len(parole) <= 30:
        return testo
    return " ".join(parole[:30]) + "..."

def parse_list_field(x):
    if pd.isna(x):
        return []
    try:
        return ast.literal_eval(x)
    except Exception:
        return []

def obiettivo_simile(lista_obiettivi, target):
    return any(fuzz.partial_ratio(o.lower(), target.lower()) >= 80 for o in lista_obiettivi)

def filtra_bandi(
    df: pd.DataFrame,
    regione: str,
    dimensione: str,
    obiettivo_preferenziale: str,
    mcc_rating: str,
    z_score: float,
    numero_dipendenti: int,
    ebitda: float,
    utile_netto: float,
    fatturato: float,
    max_results: int = 30
) -> list:
    logger.info("✅ Inizio filtra_bandi() COMPLETO")

    # Pulizia stringhe
    df["titolo_clean"] = df["Titolo"].astype(str).str.strip()
    df["descrizione_clean"] = df["Descrizione"].astype(str).str.strip()
    df["data_chiusura_clean"] = df["Data_chiusura"].astype(str).str.strip()
    df["forma_agevolazione_clean"] = df["Forma_agevolazione"].astype(str).str.strip()

    # Parsing liste
    df["dimensioni_list"] = df["Dimensioni"].apply(parse_list_field)
    df["regioni_list"] = df["Regioni"].apply(parse_list_field)
    df["obiettivo_list"] = df["Obiettivo_Finalita"].apply(parse_list_field)

    obiettivo_clean = obiettivo_preferenziale.strip()
    dimensione_clean = dimensione.strip()
    regione_clean = regione.strip()

    # Solvibilità critica
    solvibilita_critica = (
        (ebitda + utile_netto) < 0
        and mcc_rating.upper() in ["CCC", "B"]
    )
    if solvibilita_critica:
        logger.info("⚠️ Solvibilità critica: filtriamo solo bandi di sostegno liquidità.")

    # Filtro scadenza
    oggi = pd.Timestamp.today()
    df["Data_chiusura_parsed"] = pd.to_datetime(df["data_chiusura_clean"], errors="coerce")
    scadenza_limite = oggi + pd.Timedelta(days=45)
    df = df[
        (df["Data_chiusura_parsed"].isna())
        | (df["Data_chiusura_parsed"] >= scadenza_limite)
    ]

    # Numero massimo dipendenti
    if "Numero_Max_Dipendenti" in df.columns:
        df["Numero_Max_Dipendenti"] = df["Numero_Max_Dipendenti"].fillna(99999)
        df = df[
            numero_dipendenti <= df["Numero_Max_Dipendenti"]
        ]

    # Fatturato minimo
    if "Fatturato_Minimo" in df.columns:
        df["Fatturato_Minimo"] = df["Fatturato_Minimo"].fillna(0)
        df = df[
            fatturato >= df["Fatturato_Minimo"]
        ]

    # Cofinanziamento minimo
    cofinanziamento_percentuale = (
        (ebitda + utile_netto) / fatturato * 100
        if fatturato > 0 else 0
    )
    if "Cofinanziamento_Minimo" in df.columns:
        df["Cofinanziamento_Minimo"] = df["Cofinanziamento_Minimo"].fillna(0)
        df = df[
            df["Cofinanziamento_Minimo"] <= cofinanziamento_percentuale
        ]

    if df.empty:
        logger.info("🚫 Nessun bando dopo i filtri preliminari.")
        return []

    # Funzione compatibilità regione
    def match_regione(l, regione):
        if not l:
            return False
        return (regione in l) or ("tutte le regioni" in [s.lower() for s in l])

    # Filtro principale
    if solvibilita_critica:
        df_selected = df[
            df["regioni_list"].apply(lambda l: match_regione(l, regione_clean))
            &
            df["obiettivo_list"].apply(lambda l: any("sostegno liquidità" in s.lower() for s in l))
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
        logger.info("🚫 Nessun bando dopo il filtro principale.")
        return []

    # Calcolo punteggio solidità
    mcc_punteggio = MCC_RATING_PUNTEGGIO.get(mcc_rating.upper(), 5)
    z_punteggio = punteggio_zscore(z_score)
    media_punteggio = (mcc_punteggio + z_punteggio) / 2

    # Ordinamento
    df_sorted = df_selected.sort_values(
        by=["Data_chiusura_parsed"],
        ascending=True
    ).head(max_results)

    # Output finale
    risultati = []
    for _, row in df_sorted.iterrows():
        descrizione_ridotta = riassunto_30_parole(row.get("descrizione_clean", ""))
        data_chiusura = row.get("data_chiusura_clean", "")
        if not data_chiusura or str(data_chiusura).strip() == "":
            data_chiusura = "bando disponibile fino ad esaurimento fondi. Verificare residuo stanziamento."

        risultati.append({
            "Titolo Bando": row.get("titolo_clean", ""),
            "Data Scadenza": data_chiusura,
            "Solidità Aziendale VS Bando": livello_coerenza_solidita(media_punteggio),
            "Motivazione Solidità": motivazione_solidita(media_punteggio),
            "Obiettivo Bando": row.get("obiettivo_list", []),
            "Prioritario SI/NO": "SI" if obiettivo_simile(row.get("obiettivo_list", []), obiettivo_clean) else "NO",
            "Percentuale Spesa": row.get("percentuale_ammissibilità") or "Non definita",
            "Tipo Agevolazione": row.get("forma_agevolazione_clean", ""),
            "Costi Ammessi": row.get("Costi_Ammessi", ""),
            "Descrizione Sintetica": descrizione_ridotta
        })

    logger.info(f"✅ JSON finale mandato a GPT: {risultati}")
    logger.info(f"✅ Bandi selezionati e inviati a eVoluto: {len(risultati)}.")
    return risultati
