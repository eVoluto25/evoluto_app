
import logging
from analisi_indici_macroarea import calcola_indici, assegna_macro_area
from scoring_bandi import calcola_punteggi_bandi

# Configura logging
logging.basicConfig(level=logging.INFO)

def step1_analisi(pdf_file):
    """Step 1: Analisi del bilancio PDF e assegnazione macroarea"""
    try:
        logging.info("Step 1: Ricevuto file PDF per analisi")

        global dati_azienda, output_analisi

        # Calcolo indici
        indici = calcola_indici(pdf_file.name)
        logging.info(f"Indici calcolati: {indici}")

        # Assegna macroarea
        macroarea = assegna_macro_area(indici)
        logging.info(f"Macroarea assegnata: {macroarea}")

        # Estrai dati anagrafici
        dati_azienda = {
            "nome_azienda": indici.get("Nome Azienda", "ND"),
            "codice_ateco": indici.get("Codice ATECO", "ND"),
            "attivita_prevalente": indici.get("Attività Prevalente", "ND"),
            "regione": indici.get("Regione", "ND"),
            "dimensione": indici.get("Dimensione", "ND"),
            "addetti": indici.get("Addetti", "ND")
        }

        # Output analisi completo
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

        return output_analisi, [], "", ""  # Bandi, csv, pdf verranno riempiti dopo

    except Exception as e:
        logging.error(f"Errore durante l'analisi: {str(e)}")
        return f"Errore durante l'analisi: {str(e)}"


def step2_matching(macroarea, dati_azienda, indici):
    """Step 2: Matching con i bandi da Supabase e calcolo punteggio"""
    try:
        bandi_trovati = calcola_punteggi_bandi(macroarea, dati_azienda, indici)
        logging.info(f"Bandi selezionati: {len(bandi_trovati)}")
        return bandi_trovati
    except Exception as e:
        logging.error(f"Errore nel matching bandi: {e}")
        return []
