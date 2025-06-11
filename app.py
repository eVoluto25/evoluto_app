
import gradio as gr
import logging
from datetime import datetime
from analisi_indici_macroarea import calcola_indici, assegna_macro_area
from modulo_punteggio import calcola_punteggi_bandi

# Configura il logging
logging.basicConfig(
    filename="log_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Variabili globali temporanee
dati_azienda = {}
output_analisi = {}

def step1_analisi(pdf_file):
    try:
        logging.info("Step 1: Ricevuto file PDF per analisi.")
        global dati_azienda
        dati_azienda = analizza_pdf(pdf_file.name)
        logging.info("Analisi finanziaria completata con successo.")
        return dati_azienda['output_indici'], dati_azienda['macroarea']
    except Exception as e:
        logging.error(f"Errore nell'analisi del file PDF: {str(e)}")
        return "Errore nell'analisi del bilancio.", ""

def step2_matching_bandi():
    try:
        if not dati_azienda:
            logging.warning("Nessun dato aziendale disponibile per il matching.")
            return "Errore: Nessuna analisi disponibile. Carica prima il PDF."

        logging.info("Step 2: Avvio ricerca bandi con Supabase.")
        bandi_trovati = calcola_punteggi_bandi(
            macroarea=dati_azienda['macroarea'],
            ateco=dati_azienda['codice_ateco'],
            regione=dati_azienda['regione'],
            dimensione=dati_azienda['dimensione'],
            ebitda_margin=dati_azienda.get('EBITDA Margin', None),
            utile_netto=dati_azienda.get('Utile Netto', None),
            debt_to_equity=dati_azienda.get('Debt/Equity', None)
        )
        logging.info(f"Trovati {len(bandi_trovati)} bandi compatibili.")
        return bandi_trovati
    except Exception as e:
        logging.error(f"Errore nella fase di matching bandi: {str(e)}")
        return f"Errore nel matching dei bandi: {str(e)}"

with gr.Blocks(title="Analisi Bilancio & Ricerca Bandi") as demo:
    gr.Markdown("## Step 1: Carica il Bilancio in PDF")
    file_input = gr.File(label="Carica PDF Bilancio", file_types=[".pdf"])
    output_indici = gr.Textbox(label="25 Indici Finanziari", lines=10)
    output_macroarea = gr.Textbox(label="Macroarea Assegnata")

    esegui_analisi_btn = gr.Button("Esegui Analisi")
    esegui_analisi_btn.click(fn=step1_analisi, inputs=[file_input], outputs=[output_indici, output_macroarea])

    gr.Markdown("---")
    gr.Markdown("## Step 2: Matching con i Bandi")
    avvia_matching_btn = gr.Button("Avvia Ricerca Bandi")
    bandi_output = gr.Dataframe(label="Top 10 Bandi Compatibili")
    avvia_matching_btn.click(fn=step2_matching_bandi, outputs=bandi_output)

if __name__ == "__main__":
    demo.launch()
