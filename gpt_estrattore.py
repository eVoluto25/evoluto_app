# gpt_estrattore.py

import requests

RENDER_GPT_URL = "https://render-gpt.example.com/estrai"
RENDER_API_KEY = "Bearer ${RENDER_GPT_API_KEY}"  # salvata su Render

def estrai_dati_pdf(file_path: str):
    headers = {"Authorization": RENDER_API_KEY}
    files = {"file": open(file_path, "rb")}
    try:
        response = requests.post(RENDER_GPT_URL, files=files, headers=headers)
        response.raise_for_status()
        return response.json()  # {"anagrafica": {...}, "bilancio": {...}}
    except Exception as e:
        return {"error": f"Errore estrazione GPT: {str(e)}"}
