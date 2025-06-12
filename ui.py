import gradio as gr
import logging
import base64
from app import step1_analisi, step2_matching

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ID e Password (caricate su Render)
USER_ID = "admin"
PASSWORD = "secure_password"

authenticated = False

with gr.Blocks(theme=gr.themes.Base(), css="""
body { background-color: #000000; }
.gr-box { background: rgba(50, 50, 50, 0.3); border-radius: 10px; padding: 20px; color: #ccc; }
.gr-button { background-color: #333; color: #fff; border-radius: 8px; }
.gr-textbox, .gr-file { background-color: #222; color: #eee; border-radius: 6px; }
#footer { font-size: 12px; color: #777; text-align: center; margin-top: 20px; }
.copy-btn { float: right; font-size: 12px; }
""") as ui:

    with gr.Column():
        login_id = gr.Textbox(label="ID", type="password")
        login_pw = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_out = gr.Textbox(label="Status Login", interactive=False)

    def check_login(user, pwd):
        global authenticated
        if user == USER_ID and pwd == PASSWORD:
            authenticated = True
            return "Accesso riuscito"
        else:
            return "Credenziali non valide"

    login_btn.click(check_login, [login_id, login_pw], login_out)

    with gr.Column(visible=False) as main_interface:
        logout_btn = gr.Button("Logout", elem_id="logout")
        pdf_input = gr.File(label="Carica il bilancio in PDF", type="file")
        analizza_btn = gr.File(label="Carica il bilancio in PDF", type="filepath", file_types=[".pdf"])

        output_analisi = gr.Textbox(label="Anagrafica e Indici Finanziari", lines=12)
        macroarea_output = gr.Textbox(label="Macro-area Assegnata")

        csv_download = gr.File(label="Scarica risultati in CSV")
        pdf_download = gr.File(label="Scarica report in PDF")

        matching_btn = gr.Button("Avvia Matching Bandi")
        matching_output = gr.Dataframe(headers=["Titolo", "Obiettivo_Finalita", "Forma_agevolazione", "Punteggio"], label="Top 10 bandi suggeriti")

        footer = gr.Markdown("""
        <div id='footer'>
        Trattamento dei dati – I file caricati vengono elaborati automaticamente e non vengono memorizzati. Nessun dato personale viene condiviso o archiviato.
        </div>
        """)

    def run_analisi(pdf):
        try:
            out_txt, macroarea, csv_path, pdf_path = step1_analisi(pdf.name)
            return out_txt, macroarea, csv_path, pdf_path
        except Exception as e:
            logging.error("Errore nell'analisi finanziaria: %s", e)
            return "Errore", "Errore", None, None

    def run_matching():
        try:
            bandi_df = step2_matching()
            top_bandi = bandi_df.head(10)
            return top_bandi
        except Exception as e:
            logging.error("Errore nel matching dei bandi: %s", e)
            return []

    analizza_btn.click(fn=run_analisi, inputs=[pdf_input], outputs=[output_analisi, macroarea_output, csv_download, pdf_download])
    matching_btn.click(fn=run_matching, inputs=[], outputs=[matching_output])

    def show_main_interface():
        return gr.update(visible=True)

    login_btn.click(fn=show_main_interface, inputs=[], outputs=[main_interface])
    logout_btn.click(fn=lambda: gr.update(visible=False), inputs=[], outputs=[main_interface])

ui.launch(server_name="0.0.0.0", server_port=7860)
