import gradio as gr
from app import step1_analisi


def run_analisi(pdf_file):
    try:
        output_analisi, bandi_trovati, csv_path, pdf_path = step1_analisi(pdf_file.name)

        testo_output = f"""
{output_analisi}

Bandi suggeriti (Top 10):\n\n"""
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
