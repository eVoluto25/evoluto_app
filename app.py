import logging
import re
from pdfminer.high_level import extract_text
from analisi_indici_macroarea import calcola_indici, assegna_macro_area
from scoring_bandi import filtra_e_valuta_bandi

logging.basicConfig(level=logging.INFO)


def estrai_dati_da_pdf(path):
    text = extract_text(path)
    mappa = {}

    for riga in text.splitlines():
        match = re.match(r"(.+?):\s+([-+]?[0-9]*[.,]?[0-9]+)", riga)
        if match:
            chiave = match.group(1).strip()
            valore = match.group(2).replace(",", ".")
            try:
                mappa[chiave] = float(valore)
            except:
                pass

    return mappa


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

        output_text = f"""Analisi Aziendale

Nome azienda: {dati_azienda['nome_azienda']}
Attività prevalente: {dati_azienda['attivita_prevalente']}
Addetti: {dati_azienda['addetti']}
Regione: {dati_azienda['regione']}
Dimensione: {dati_azienda['dimensione']}
Codice ATECO: {dati_azienda['codice_ateco']}

Macroarea assegnata: {macroarea}

Indici calcolati:
""" + "\n".join([f"{k}: {v}" for k, v in indici.items()])

        return output_analisi, [], "", ""

    except Exception as e:
        logging.error(f"Errore durante l'analisi: {str(e)}")
        return f"Errore durante l'analisi: {str(e)}"


def step2_matching(macroarea, dati_azienda, indici):
    try:
        bandi_trovati = filtra_e_valuta_bandi(bandi, dati_azienda)
        logging.info(f"Bandi selezionati: {len(bandi_trovati)}")
        return bandi_trovati
    except Exception as e:
        logging.error(f"Errore nel matching bandi: {e}")
        return []
