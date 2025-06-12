import gradio as gr
import os
from app import step1_analisi

# Preleva le credenziali da Render (variabili d'ambiente)
USERNAME = os.getenv("EVOLUTO_USERNAME")
PASSWORD = os.getenv("EVOLUTO_PASSWORD")

# Funzione di autenticazione
def login(user, pwd):
    if user == USERNAME and pwd == PASSWORD:
        return gr.update(visible=False), gr.update(visible=True)
    return gr.update(value="", visible=True), gr.update(visible=False)

# Placeholder per la funzione di avvio processo
def avvia_processamento(file):
    if file is None:
        return "Nessun file caricato."
    return step1_analisi(file)

with gr.Blocks(css="""
body { background-color: #1e1e1e; color: #f0f0f0; font-family: 'Arial', sans-serif; }
button, input, textarea { border-radius: 12px !important; }
.gr-button { background-color: #333333 !important; color: white; border: none; padding: 12px 24px; font-size: 16px; }
.gr-button:hover { background-color: #4b4b4b !important; }
footer { color: #999999; font-size: 12px; text-align: center; margin-top: 20px; }
""") as demo:

    # Login
    with gr.Column(visible=True) as login_area:
        user = gr.Textbox(label=None, placeholder="ID utente", type="password")
        pwd = gr.Textbox(label=None, placeholder="Password", type="password")
        login_btn = gr.Button("Login")
        login_btn.click(fn=login, inputs=[user, pwd], outputs=[login_area, "main_ui"])

    # UI principale
    with gr.Column(visible=False, elem_id="main_ui") as main_ui:
        upload = gr.File(label=None, file_types=[".pdf"], type="file")
        start_btn = gr.Button("Avvia eVoluto")
        output = gr.Textbox(label=None, interactive=False)
        start_btn.click(fn=avvia_processamento, inputs=upload, outputs=output)

        # Footer per trattamento dati
        gr.Markdown("""
        I dati caricati vengono elaborati automaticamente e non vengono memorizzati.
        Nessun dato personale viene condiviso o archiviato.
        """)

demo.launch()
