import gradio as gr
import logging
import os
from datetime import datetime

from analisi_indici_macroarea import calcola_indici, assegna_macro_area
from modulo_punteggio import calcola_punteggi_bandi

port = int(os.environ.get("PORT", 7860))  # Porta gestita da Render

logging.basicConfig(
    filename="log_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

dati_azienda = {}
output_analisi = {}

def step1_analisi(pdf_file):
    try:
        logging.info("Step 1: Ricevuto file PDF per analisi")
        global dati_azienda, output_analisi

        # Step 3A – Calcolo indici
        indici = calcola_indici(pdf_file.name)
        logging.info(f"Indici calcolati: {indici}")

        # Step 3B – Assegnazione macroarea
        macroarea = assegna_macro_area(indici)
        logging.info(f"Macroarea assegnata: {macroarea}")

        # Step 3C – Dati aziendali identificativi
        dati_azienda = {
            "nome_azienda": indici.get("Nome Azienda", "ND"),
            "codice_ateco": indici.get("Codice ATECO", "ND"),
            "attivita_prevalente": indici.get("Attività Prevalente", "ND"),
            "regione": indici.get("Regione", "ND"),
            "dimensione": indici.get("Dimensione", "ND"),
            "addetti": indici.get("Addetti", "ND")
        }

        output_analisi = {
            "Macroarea": macroarea,
            "Indici calcolati": indici
        }

        # Step 3D – Output formattato
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

interfaccia = gr.Interface(
    fn=step1_analisi,
    inputs=gr.File(label="Carica il bilancio in PDF"),
    outputs=gr.Textbox(label="Risultato Analisi Finanziaria"),
    title="eVoluto – Analisi Finanziaria Automatica",
    description="Carica un bilancio PDF. eVoluto eseguirà l'analisi completa e assegnerà la macroarea di intervento."
)

print("Gradio pronto all'avvio")
interfaccia.launch(server_name="0.0.0.0", server_port=port)
print("Interfaccia lanciata")
