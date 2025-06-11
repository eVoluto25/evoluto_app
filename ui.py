import gradio as gr

def build_interface(main_fn):
    css = """
    body {
        background-color: #f7f8fa;
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    .gradio-container {
        padding: 20px !important;
    }
    .custom-title {
        font-size: 24px;
        font-weight: 600;
        color: #202123;
        margin-bottom: 1rem;
    }
    """

    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="green",
        neutral_hue="gray",
        radius_size="lg",
        text_size="lg"
    )

    with gr.Blocks(css=css, theme=theme) as demo:
        gr.Markdown("<div class='custom-title'>\u2728 eVoluto</div>")

        with gr.Row():
            with gr.Column(scale=1):
                file = gr.File(file_types=[".pdf"], label=None, show_label=False)
                analyze_btn = gr.Button("Avvia Analisi", variant="primary")

            with gr.Column(scale=2):
                macroarea = gr.Textbox(label="Macroarea assegnata", interactive=False)
                scores = gr.Textbox(label="Punteggi macroaree (Crisi / Crescita / Espansione)", lines=2, interactive=False)
                indices = gr.Textbox(label="25 Indici Finanziari", lines=8, interactive=False)
                top_bandi = gr.Dataframe(
                    headers=["Titolo", "Punteggio", "Scadenza", "Regione"],
                    label="Top 10 Bandi Consigliati"
                )
                csv_file = gr.File(label="Scarica risultati in CSV")
                pdf_file = gr.File(label="Scarica report in PDF")

        analyze_btn.click(
            fn=main_fn,
            inputs=file,
            outputs=[macroarea, scores, indices, top_bandi, csv_file, pdf_file]
        )

        gr.Markdown(
            '''
            <div style="text-align: center; font-size: 14px; color: #6b7280; padding-top: 20px;">
            ⚪️ <strong>Trattamento dei dati</strong> ⚪️<br>
            I file caricati vengono elaborati automaticamente e non vengono memorizzati.<br>
            Nessun dato personale viene condiviso o archiviato.
            </div>
            '''
        )

    return demo
