
import gradio as gr
import os
from app import step1_analisi

USERNAME = os.getenv("EVOLUTO_USERNAME")
PASSWORD = os.getenv("EVOLUTO_PASSWORD")

def login(user, pwd):
    if user == USERNAME and pwd == PASSWORD:
        return gr.update(visible=False), gr.update(visible=True)
    return gr.update(value="", visible=True), gr.update(visible=False)

def avvia_processamento(file):
    if file is None:
        return "Nessun file caricato.", "", "", "", "", ""
    output = step1_analisi(file)
    return output, "", "", "", "", ""

with gr.Blocks(css="""
body { background-color: #f1f1f1; font-family: 'Arial', sans-serif; }
.gr-button { background-color: #333 !important; color: white !important; border: none; padding: 10px 20px; font-size: 14px; }
.gr-button:hover { background-color: #4b4b4b !important; }
footer { color: #999; font-size: 12px; text-align: center; margin-top: 20px; }
""") as demo:

    with gr.Column(visible=True, elem_id="login-panel") as login_panel:
        user_input = gr.Textbox(label="Username")
        pass_input = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Avvia eVoluto")

    with gr.Column(visible=False, elem_id="main-panel") as main_panel:

        file_input = gr.File(label="Carica bilancio", file_types=[".pdf"])

        # Finestra anagrafica
        anagrafica = gr.Textbox(label="Anagrafica azienda", lines=3)

        # Analisi finanziaria completa con indici
        analisi_finanziaria = gr.Textbox(label="Analisi finanziaria", lines=25, show_copy_button=True)

        # Macro area
        macroarea_box = gr.Textbox(label="Macro area assegnata", lines=2, show_copy_button=True)
        match_button = gr.Button("Trova bandi")

        # Bandi selezionati
        bandi_box = gr.Textbox(label="Bandi selezionati", lines=8, show_copy_button=True)

        # Relazione analitica e predittiva
        commento_box = gr.Textbox(label="Relazione analista", lines=6, show_copy_button=True)

        file_input.change(fn=avvia_processamento, inputs=file_input,
                          outputs=[analisi_finanziaria, anagrafica, macroarea_box, bandi_box, commento_box])

        match_button.click(fn=step2_bandi, inputs=[], outputs=bandi_box)

        gr.Markdown("Trattamento dei dati: i file caricati vengono elaborati automaticamente e non vengono memorizzati.", elem_id="footer")

    login_button.click(fn=login, inputs=[user_input, pass_input], outputs=[login_panel, main_panel])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
