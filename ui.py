import gradio as gr
import pandas as pd
import os
from app import step1_analisi

USERNAME = os.getenv("EVOLUTO_USERNAME")
PASSWORD = os.getenv("EVOLUTO_PASSWORD")

# Placeholder dati iniziali
anagrafica_placeholder = "Dati anagrafici azienda non ancora disponibili."
indici_placeholder = "Indici non calcolati. Caricare un bilancio."
macroarea_placeholder = "Macro-area non ancora assegnata."
bandi_placeholder = pd.DataFrame(columns=["Titolo", "Obiettivo_Finalita", "Forma_agevolazione", "Punteggio"])

with gr.Blocks(css="""
body {
    background-color: #121212;
    color: #D3D3D3;
    font-family: 'Segoe UI', sans-serif;
}
.gr-button {
    background-color: rgba(50, 50, 50, 0.8);
    border-radius: 12px;
    color: white;
}
.gr-textbox, .gr-text, .gr-file, .gr-dataframe {
    background-color: rgba(40, 40, 40, 0.6);
    border-radius: 12px;
    color: white;
}
.gr-box {
    background-color: rgba(60, 60, 60, 0.5);
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #333;
    color: white;
}
footer {
    text-align: center;
    font-size: 0.8em;
    margin-top: 30px;
    color: gray;
}
.logout-button {
    position: absolute;
    top: 10px;
    right: 10px;
}
""") as ui:

    # Pulsante Logout
    with gr.Row():
        gr.Button("Logout", elem_classes="logout-button")

    # Step 1: Analisi Finanziaria
    with gr.Row():
        with gr.Column():
            with gr.Group():
                anagrafica = gr.Textbox(label="Anagrafica Azienda", value=anagrafica_placeholder, lines=5, interactive=False, show_copy_button=True)
            with gr.Group():
                indici = gr.Textbox(label="25 Indici Finanziari", value=indici_placeholder, lines=15, interactive=False, show_copy_button=True)
        with gr.Column():
            with gr.Group():
                macroarea = gr.Textbox(label="Macro Area Assegnata", value=macroarea_placeholder, interactive=False, show_copy_button=True)
            with gr.Row():
                btn_csv = gr.Button("Scarica risultati in CSV")
                btn_pdf = gr.Button("Scarica report in PDF")

    # Step 2: Matching Bandi
    with gr.Group():
        btn_matching = gr.Button("Avvia Matching Bandi")
        tabella_bandi = gr.Dataframe(value=bandi_placeholder, headers=["Titolo", "Obiettivo_Finalita", "Forma_agevolazione", "Punteggio"], interactive=False, label="Top 10 Bandi Ordinati per Punteggio")

    # Upload documento (spostato in basso)
    with gr.Group():
        file_input = gr.File(label="Carica il bilancio in PDF", file_types=['.pdf'])

    # Footer trattamento dati
    gr.Markdown("""
        <footer>
            Trattamento dei dati – I file caricati vengono elaborati automaticamente e non vengono memorizzati. Nessun dato personale viene condiviso o archiviato.
        </footer>
    """)

ui.launch()
