import gradio as gr
from app import step1_analisi, step2_matching

# Funzione per analizzare il PDF e restituire l'analisi completa
def run_analisi(pdf_file):
    if pdf_file is None:
        return "Nessun file caricato."

    output_analisi, bandi_trovati, csv_path, pdf_path = step1_analisi(pdf)
    
    testo_bandi = "\n\nTOP 10 BANDI SUGGERITI:\n"
    for b in bandi_trovati[:10]:
        testo_bandi += f"\n- {b.get('Titolo', '')} | {b.get('Obiettivo_Finalita', '')} | {b.get('Forma_agevolazione', '')} | Punteggio: {b.get('score', 0)}"

    # Formatta l'intero output come testo
    analisi_completa = f"""
--- ANALISI COMPLETA ---

**Anagrafica e Indici**

{output_analisi.get('Indici calcolati', '')}

**Macroarea assegnata:** {output_analisi.get('Macroarea', '')}
{testo_bandi}
"""
    return analisi_completa

# UI Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Analisi PDF e Bandi")

    with gr.Row():
        pdf_input = gr.File(label="Carica il bilancio in PDF", file_types=[".pdf"])
        avvia_btn = gr.Button("Avvia Analisi")

    output_box = gr.Textbox(label="Risultato Analisi Completa", lines=30, show_copy_button=True)

    avvia_btn.click(fn=run_analisi, inputs=[pdf_input], outputs=[output_box])

demo.launch(server_name="0.0.0.0", server_port=7860)
