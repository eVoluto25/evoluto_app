# gpt_estrattore.py

import requests
import os
import logging

GPT_API_URL = os.getenv("RENDER_GPT_URL", "https://render-gpt.example.com/estrai")
GPT_API_KEY = os.getenv("RENDER_GPT_API_KEY")

def estrai_dati_pdf(file_path: str) -> dict:
    headers = {
        "Authorization": f"Bearer {GPT_API_KEY}"
    }

    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/pdf")}
            response = requests.post(GPT_API_URL, headers=headers, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()
            if "anagrafica" not in result or "bilancio" not in result:
                return {"errore": "JSON estratto non valido"}
            return result
    except Exception as e:
        logging.error(f"Errore estrazione GPT: {e}")
        return {"errore": str(e)}