# ui.py
import os
import gradio as gr
import requests
import json

API_URL = "https://evoluto.onrender.com"  # Cambia con il tuo dominio reale se diverso

def analizza_file(file):
    with open(file.name, "rb") as f:
        files = {"file": f}
        res = requests.post(f"{API_URL}/upload", files=files)
    if res.status_code != 200:
        return f"Errore upload: {res.text}", None

    azienda = res.json()
    id_bando = "TEST_001"
    payload = {
        "azienda": azienda,
        "id_bando": id_bando
    }
    res2 = requests.post(f"{API_URL}/score", json=payload)
    if res2.status_code != 200:
        return f"Errore score: {res2.text}", None

    return "Analisi completata", json.dumps(res2.json(), indent=2)

with gr.Blocks(title="eVoluto – Sistema Matching Bandi") as demo:
    gr.Markdown("# 📊 eVoluto – Analisi automatica bilanci e bandi")
    file_input = gr.File(label="Carica PDF Bilancio/Visura", file_types=[".pdf"])
    button = gr.Button("Analizza e Calcola Score")
    output_json = gr.Textbox(label="Output JSON (score + macroarea)", lines=25)
    status = gr.Textbox(label="Esito", max_lines=1)

    button.click(fn=analizza_file, inputs=file_input, outputs=[status, output_json])

port = int(os.environ.get("PORT", 10000))
demo.launch(server_name="0.0.0.0", server_port=port)
