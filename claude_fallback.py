# claude_fallback.py

import requests

RENDER_CLAUDE_URL = "https://render-claude.example.com/fallback"
RENDER_API_KEY = "Bearer ${RENDER_CLAUDE_API_KEY}"  # salvata su Render

def invia_a_claude(payload: dict):
    headers = {
        "Authorization": RENDER_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(RENDER_CLAUDE_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()  # {"macroarea_validata": ..., "motivazione": ...}
    except Exception as e:
        return {"error": f"Errore chiamata Claude: {str(e)}"}
