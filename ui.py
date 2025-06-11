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
    input[type='file'] + div {
        display: none !important;
    }
    .gr-file .file-preview {
        display: none !important;
    }
    """

    theme = gr.themes.Soft(
        primary_hue="gray",
        secondary_hue="blue",
        neutral_hue="slate",
        radius_size="lg",
        text_size="lg"
    )

    with gr.Blocks(css=css, theme=theme) as demo:
        with gr.Row():
            with gr.Column(scale=2):
                macroarea = gr.Textbox(label="Macroarea assegnata", interactive=False)
                indices = gr.Textbox(label="25 Indici Finanziari", lines=8, interactive=False)
                csv_file = gr.File(label="Scarica risultati in CSV", interactive=False)
                pdf_file = gr.File(label="Scarica report in PDF", interactive=False)
                file = gr.File(label="", file_types=[".pdf"])
                analyze_btn = gr.Button("Avvia eVoluto", variant="primary")

        analyze_btn.click(
            fn=main_fn,
            inputs=file,
            outputs=[macroarea, indices, csv_file, pdf_file]
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
