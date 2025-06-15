import os
import requests
import json
from config import ANTHROPIC_API_KEY
from prompt_claude import PROMPT_CLAUDE_BASE

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

def chiama_claude(bandi_filtrati, z_score, mcc_rating, utile_netto):
    prompt = PROMPT_CLAUDE_BASE.format(
        z_score=z_score,
        mcc_rating=mcc_rating,
        utile_netto=utile_netto,
        bandi=json.dumps(bandi_filtrati, ensure_ascii=False, indent=2)
    )

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-3-opus-20240229",
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
