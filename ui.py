import gradio as gr
from app import step1_analisi

def run_analisi(file):
    try:
        if hasattr(file, 'tempfile'):
            class FileMock:
                name = file.tempfile
            result = step1_analisi(FileMock())
        else:
            return "Formato file non valido"

        if isinstance(result, str):
            return result

        output, *_ = result
        indici = output.get("Indici calcolati", {})
        macroarea = output.get("Macroarea", "ND")

        out = f"✅ Macroarea assegnata: {macroarea}\n\n📊 Indici calcolati:\n"
        out += "\n".join([f"- {k}: {v}" for k, v in indici.items()])
        return out

    except Exception as e:
        return f"Errore durante l'analisi: {str(e)}"

with gr.Blocks() as ui:
    with gr.Row():
        pdf_input = gr.File(label="Carica il bilancio PDF", file_types=[".pdf"])

    with gr.Row():
        output_box = gr.Textbox(label="Analisi completata", lines=30, interactive=False, show_copy_button=True)

    with gr.Row():
        analizza_btn = gr.Button("Avvia Analisi")

    analizza_btn.click(fn=run_analisi, inputs=[pdf_input], outputs=[output_box])

ui.launch(server_name="0.0.0.0", server_port=7860)
