# claude_fallback.py

import requests
import os
import logging

CLAUDE_API_URL = os.getenv("RENDER_CLAUDE_URL", "https://render-claude.example.com/fallback")
CLAUDE_API_KEY = os.getenv("RENDER_CLAUDE_API_KEY")

def invia_a_claude(payload: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(CLAUDE_API_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        risultato = response.json()
        if "macroarea_validata" not in risultato:
            return {"errore": "Claude non ha restituito macroarea_validata"}
        return {
            "macroarea_validata": risultato.get("macroarea_validata"),
            "motivazione": risultato.get("motivazione", "N/D")
        }
    except Exception as e:
        logging.error(f"Errore Claude fallback: {e}")
        return {"errore": str(e), "macroarea_validata": None, "motivazione": None}