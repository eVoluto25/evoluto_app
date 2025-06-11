import gradio as gr

css = """
footer.svelte-1ipelgc {
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

def build_interface(fn):
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
            fn=fn,
            inputs=file,
            outputs=[macroarea, indices, csv_file, pdf_file]
        )
    return demo
