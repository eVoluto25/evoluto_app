import logging
from analisi_indici_macroarea import calcola_indici, assegna_macro_area
from scoring_bandi import calcola_punteggi_bandi

# Configura logging
logging.basicConfig(
    filename="log_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Variabili globali temporanee
dati_azienda = {}
output_analisi = {}

# Funzione principale di analisi
def step1_analisi(pdf_file):
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
""" + "\n".join([f"- {k}: {v}" for k, v in indici.items()])

        return output_text

    except Exception as e:
        logging.error(f"Errore durante l'analisi: {str(e)}")
        return f"Errore durante l'analisi: {str(e)}"
