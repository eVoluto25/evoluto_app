
import gradio as gr
import logging
from app import step1_analisi, step2_matching

# Impostazioni login
USER_ID = "admin"
PASSWORD = "secure_password"
authenticated = False

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
        login_status = gr.Textbox(label="Status Login", interactive=False)

    def check_login(user, pwd):
        global authenticated
        if user == USER_ID and pwd == PASSWORD:
            authenticated = True
            return "Accesso riuscito"
        else:
            return "Credenziali non valide"

    login_btn.click(fn=check_login, inputs=[login_id, login_pw], outputs=login_status)

    with gr.Column(visible=False) as main_interface:
        logout_btn = gr.Button("Logout", elem_id="logout")

        pdf_input = gr.File(label="Carica il bilancio in PDF", file_types=[".pdf"])
        analizza_btn = gr.Button("Avvia eVoluto")

        output_analisi = gr.Textbox(label="Anagrafica e 25 Indici Finanziari", lines=12, show_copy_button=True)
        macroarea_output = gr.Textbox(label="Macro-area Assegnata", show_copy_button=True)

        csv_download = gr.File(label="Scarica risultati in CSV")
        pdf_download = gr.File(label="Scarica report in PDF")

        matching_btn = gr.Button("Avvia Matching Bandi")
        matching_output = gr.Dataframe(headers=["Titolo", "Obiettivo_Finalita", "Forma_agevolazione", "Punteggio"],
                                       label="Top 10 bandi suggeriti", interactive=False)

        footer = gr.Markdown("""
        <div id="footer">
        Trattamento dei dati – I file caricati vengono elaborati automaticamente e non vengono memorizzati.
        Nessun dato personale viene condiviso o archiviato.
        </div>
        """)

    def run_analisi(file):
        output, bandi, csv_path, pdf_path = step1_analisi(file)
        return output, bandi["Macroarea"], csv_path, pdf_path

    def run_matching(macroarea, dati, indici):
        bandi = step2_matching(macroarea, dati, indici)
        return bandi[:10]  # top 10 bandi

    analizza_btn.click(fn=run_analisi, inputs=[pdf_input],
                       outputs=[output_analisi, macroarea_output, csv_download, pdf_download])

    matching_btn.click(fn=run_matching, inputs=[macroarea_output, output_analisi, output_analisi],
                       outputs=matching_output)

    def toggle_visibility(status):
        return gr.update(visible=status)

    login_btn.click(fn=lambda u, p: authenticated, inputs=[login_id, login_pw], outputs=[], show_progress=False)
    login_btn.click(fn=toggle_visibility, inputs=[login_id, login_pw], outputs=[main_interface])

ui.launch(server_name="0.0.0.0", server_port=7860)
