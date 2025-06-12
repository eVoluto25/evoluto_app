import logging
import re
from pdfminer.high_level import extract_text
from analisi_indici_macroarea import calcola_indici, assegna_macro_area
from scoring_bandi import filtra_e_valuta_bandi

logging.basicConfig(level=logging.INFO)

def estrai_dati_da_pdf(path):
    text = extract_text(path)
    mappa = {}

    def estrai_valore(riga):
        numeri = re.findall(r"[-+]?[0-9]{1,3}(?:\.[0-9]{3})*(?:,[0-9]+)?", riga)
        if numeri:
            return float(numeri[0].replace(".", "").replace(",", "."))
        return None

    mappatura = {
        "Patrimonio Netto": "Totale patrimonio netto",
        "Debiti": "Totale debiti",
        "Attività a breve": "Totale attivo circolante",
        "Attività liquide": "Disponibilità liquide",
        "Rimanenze": "Rimanenze",
        "Passività a breve": "esigibili entro l'esercizio successivo",
        "Passività a lungo": "esigibili oltre l'esercizio successivo",
        "Totale Attivo": "Totale attivo",
        "Totale Passivo": "Totale passivo",
        "Ricavi": "ricavi delle vendite e delle prestazioni",
        "Risultato Netto": "Utile (perdita) dell'esercizio",
        "Oneri Finanziari": "interessi e altri oneri finanziari",
        "Risultato Operativo": "Differenza tra valore e costi della produzione",
        "Margine Operativo Lordo": "Differenza tra valore e costi della produzione",
    }

    for campo, label in mappatura.items():
        for riga in text.splitlines():
            if label.lower() in riga.lower():
                val = estrai_valore(riga)
                if val is not None:
                    mappa[campo] = val
                    break

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
