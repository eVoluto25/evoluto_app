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
    .section-box {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    """

    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="green",
        neutral_hue="gray",
        radius_size="xl",
        text_size="lg"
    )

    with gr.Blocks(css=css, theme=theme) as demo:
        gr.Markdown("<div class='custom-title'>\u2728 Analisi Finanziaria e Ricerca Bandi</div>")
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Box(elem_classes="section-box"):
                    file = gr.File(label="Carica il PDF del bilancio", file_types=[".pdf"])
                    analyze_btn = gr.Button("Avvia Analisi", variant="primary")
            with gr.Column(scale=2):
                with gr.Box(elem_classes="section-box"):
                    macroarea = gr.Textbox(label="Macroarea assegnata", interactive=False)
                    scores = gr.Textbox(label="Punteggi macroaree (Crisi / Crescita / Espansione)", lines=2, interactive=False)
                    indices = gr.Textbox(label="25 Indici Finanziari", lines=8, interactive=False)
                    top_bandi = gr.Dataframe(headers=["Titolo", "Punteggio", "Scadenza", "Regione"], label="Top 10 Bandi Consigliati")
                with gr.Box(elem_classes="section-box"):
                    csv_file = gr.File(label="Scarica risultati in CSV")
                    pdf_file = gr.File(label="Scarica report in PDF")

        analyze_btn.click(
            fn=main_fn,
            inputs=file,
            outputs=[macroarea, scores, indices, top_bandi, csv_file, pdf_file]
        )

    return demo
