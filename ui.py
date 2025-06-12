import gradio as gr
from app import step1_analisi

def run_analisi(file):
    try:
        file_path = None

        # Compatibilità Gradio Web e CLI
        if hasattr(file, 'name') and isinstance(file.name, str):
            file_path = file.name
        elif hasattr(file, 'tempfile'):
            file_path = file.tempfile

        if not file_path:
            return "Formato file non valido"

        class FileMock:
            name = file_path

        result = step1_analisi(FileMock())

        if isinstance(result, str):
            return result

        output, *_ = result
        indici = output.get("Indici calcolati", {})
        macroarea = output.get("Macroarea", "ND")

        out = f"✅ Macroarea assegnata: {macroarea}\n\n📊 Indici calcolati:\n"
        out += "\n".join([f"- {k}: {v if v not in [None, ''] else 'ND'}" for k, v in indici.items()])
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
