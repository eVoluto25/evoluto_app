import logging
import re
from pdfminer.high_level import extract_text
from analisi_indici_macroarea import calcola_indici, assegna_macro_area
from scoring_bandi import filtra_e_valuta_bandi

logging.basicConfig(level=logging.INFO)

def estrai_dati_da_pdf(path):
    text = extract_text(path)
    mappa = {}

    # Identifica l'anno più recente nel testo (es. 2024)
    match_anni = re.findall(r"20[0-9]{2}", text)
    anni = sorted(set(int(a) for a in match_anni if 2020 <= int(a) <= 2099), reverse=True)
    anno_riferimento = str(anni[0]) if anni else None
    logging.info(f"Anno identificato nel documento: {anno_riferimento}")

    def estrai_valore_per_anno(riga):
        numeri = re.findall(r"[-+]?[0-9]{1,3}(?:\.[0-9]{3})*(?:,[0-9]+)?", riga)
        if len(numeri) >= 1:
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
        "Ricavi": "ricavi delle vendite e delle prestazioni",
        "Risultato Netto": "Utile (perdita) dell'esercizio",
        "Oneri Finanziari": "interessi e altri oneri finanziari",
        "Risultato Operativo": "Differenza tra valore e costi della produzione",
        "Margine Operativo Lordo": "Differenza tra valore e costi della produzione",
        "EBITDA": "Differenza tra valore e costi della produzione",
        "NOPAT": "Utile (perdita) dell'esercizio"
    }

    righe = text.splitlines()
    for campo, label in mappatura.items():
        for riga in righe:
            if label.lower() in riga.lower():
                val = estrai_valore_per_anno(riga)
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
