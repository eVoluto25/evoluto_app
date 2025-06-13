import logging
import re
import pdfplumber
from supabase_connector import fetch_bandi
from analisi_indici_macroarea import calcola_indici, assegna_macro_area
from scoring_bandi import filtra_e_valuta_bandi
from scoring_bandi import filtra_e_valuta_bandi

bandi = fetch_bandi()

logging.basicConfig(level=logging.INFO)

def estrai_dati_da_pdf(path):
    mappa = {}

    def normalizza_label(label):
        return str(label).strip().lower().replace("€", "").replace(":", "")

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 2:
                        continue
                    label = normalizza_label(row[0])
                    val_raw = str(row[1]).strip().replace(".", "").replace(",", ".")
                    try:
                        val = float(val_raw)
                        mappa[label] = val
                    except:
                        continue

    # Mappatura logica: etichette cercate → label reali nel documento
    chiavi = {
        "Ricavi": "ricavi delle vendite e delle prestazioni",
        "Risultato Netto": "utile (perdita) dell'esercizio",
        "Oneri Finanziari": "interessi e altri oneri finanziari",
        "EBITDA": "differenza tra valore e costi della produzione",
        "Totale Attivo": "totale attivo",
        "Totale Passivo": "totale passivo",
        "Patrimonio Netto": "totale patrimonio netto",
        "Disponibilità liquide": "disponibilità liquide",
        "Rimanenze": "rimanenze",
        "Debiti": "totale debiti"
    }

    estratti = {}
    for campo, chiave_mappa in chiavi.items():
        for key in mappa:
            if chiave_mappa in key:
                estratti[campo] = mappa[key]
                break

    logging.info(f"Valori estratti da PDF: {estratti}")
    return estratti

def step1_analisi(pdf_file):
    try:
        logging.info("Step 1: Ricevuto file PDF per analisi")

        global dati_azienda, output_analisi

        dati = estrai_dati_da_pdf(pdf_file.name)
        logging.info(f"Dati grezzi estratti: {list(dati.keys())}")

        indici = calcola_indici(dati)
        logging.info(f"Indici calcolati: {indici}")

        macroarea = assegna_macro_area(indici)
        logging.info(f"Macroarea assegnata: {macroarea}")
        bandi_trovati = filtra_e_valuta_bandi(macroarea, indici, dati_azienda, bandi)

        dati_azienda = {
            "nome_azienda": indici.get("Nome Azienda", "ND"),
            "codice_ateco": indici.get("Codice ATECO", "ND"),
            "attivita_prevalente": indici.get("Attività Prevalente", "ND"),
            "regione": indici.get("Regione", "ND"),
            "dimensione": indici.get("Dimensione", "ND"),
            "addetti": indici.get("Addetti", "ND"),
            "macroarea": macroarea,
            "indici": indici
        }

        output_analisi = {
            "Macroarea": macroarea,
            "Indici calcolati": indici
        }

        return output_analisi, [], "", ""

    except Exception as e:
        logging.error(f"Errore durante l'analisi: {str(e)}")
        return f"Errore durante l'analisi: {str(e)}"

def step2_matching(macroarea, dati_azienda, indici):
    try:
        bandi_trovati = filtra_e_valuta_bandi(macroarea, indici, dati_azienda)
        logging.info(f"Bandi selezionati: {len(bandi_trovati)}")
        return bandi_trovati
    except Exception as e:
        logging.error(f"Errore nel matching bandi: {e}")
        return []
