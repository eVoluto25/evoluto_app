import os
import requests
import json
from config import CLAUDE_KEY
from prompt_claude import PROMPT_CLAUDE

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

    prompt = PROMPT_CLAUDE.format(
    macro_area=macro_area,
    dimensione=dimensione,
    codice_ateco=codice_ateco,
    regione=regione,
    ebitda=ebitda,
    utile_netto=utile_netto,
    mcc=mcc_rating,
    z_score=z_score,
    bandi=bandi_filtrati_json
    )

    headers = {
        "x-api-key": CLAUDE_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1500,
        "temperature": 0.3,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(CLAUDE_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return {"errore": f"Claude API error: {response.status_code} – {response.text}"}

    try:
        data = response.json()
        return json.loads(data["content"])  # Claude deve rispondere con JSON puro
    except Exception as e:
        return {"errore": f"Errore parsing Claude: {e}"}
