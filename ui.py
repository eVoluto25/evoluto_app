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
        return "Nessun file caricato."
    return step1_analisi(file)

with gr.Blocks(css="""
body {
    background-color: #f9f9f9;
    font-family: 'Segoe UI', sans-serif;
    color: #111;
    margin: 0;
    padding: 0;
}

button, input, textarea {
    border-radius: 12px !important;
    font-size: 16px !important;
}

#login-panel, #main-panel {
    max-width: 600px;
    margin: 80px auto;
    padding: 30px;
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

#footer {
    text-align: center;
    font-size: 12px;
    color: #888;
    margin-top: 40px;
}
""") as demo:

    with gr.Column(visible=True, elem_id="login-panel") as login_panel:
        gr.Markdown("<h2 style='text-align:center;'>Login eVoluto</h2>")
        user_input = gr.Textbox(label="Username")
        pass_input = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Avvia eVoluto")
        login_button.click(fn=login, inputs=[user_input, pass_input], outputs=[login_panel, main_panel])

    with gr.Column(visible=False, elem_id="main-panel") as main_panel:
        gr.Markdown("<h2 style='text-align:center;'>eVoluto – Analisi Finanziaria Automatica</h2>")
        gr.Markdown("Carica un bilancio PDF per ricevere l'analisi automatica dell’azienda.")

        file_input = gr.File(label="", file_types=[".pdf"])
        output_box = gr.Textbox(label="", lines=28, show_copy_button=True)

        file_input.change(fn=avvia_processamento, inputs=file_input, outputs=output_box)

        gr.Markdown("Trattamento dei dati: i file caricati vengono elaborati automaticamente e non vengono memorizzati.", elem_id="footer")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
