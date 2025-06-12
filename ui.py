import gradio as gr
from analisi_indici_macroarea import estrai_dati_bilancio
from scoring_bandi import assegna_macroarea
from app import trova_bandi_rilevanti
from pdfminer.high_level import extract_text

def carica_pdf(file):
    try:
        if hasattr(file, 'name'):
            file_path = file.name
        elif isinstance(file, str):
            file_path = file
        else:
            raise ValueError("Formato file non valido")

        text = extract_text(file_path)
        return text
    except Exception as e:
        return f"Errore durante l'analisi: {e}"

def run_analisi(file):
    try:
        testo = carica_pdf(file)
        if not isinstance(testo, str) or testo.startswith("Errore"):
            return testo

        dati = estrai_dati_bilancio(testo)
        risultato = assegna_macroarea(dati)
        bandi_trovati = trova_bandi_rilevanti(risultato["macroarea"])

        testo_output = f"""
📊 Dati di bilancio rilevati:
{dati}

🏆 Punteggi macroaree:
{risultato['punteggi']}

✅ Macroarea assegnata:
{risultato['macroarea']}

Bandi suggeriti (Top 10):\n"""
        for bando in bandi_trovati[:10]:
            testo_output += f"- {bando['Titolo']} ({bando['Punteggio']})\n"

        return testo_output

    except Exception as e:
        return f"Errore durante l'analisi: {str(e)}"

with gr.Blocks() as ui:
    with gr.Row():
        pdf_input = gr.File(label="Carica il bilancio PDF", file_types=[".pdf"])

    with gr.Row():
        output_box = gr.Textbox(label="Analisi completa", lines=30, interactive=False, show_copy_button=True)

    with gr.Row():
        analizza_btn = gr.Button("Avvia Analisi")

    analizza_btn.click(fn=run_analisi, inputs=[pdf_input], outputs=[output_box])

ui.launch(server_name="0.0.0.0", server_port=7860)
