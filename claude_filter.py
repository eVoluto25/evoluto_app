
import os
import json
import openai
from supabase import create_client, Client

# Variabili ambiente da Render
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def estrai_bandi_completi(nome_view: str):
    """Estrae tutti i dati dei bandi dalla view macroarea."""
    response = supabase.table(nome_view).select("*").execute()
    return response.data

def costruisci_prompt_completo(bandi: list, azienda: dict) -> str:
    intestazione = (
        f"Contesto azienda:\n"
        f"- Macroarea: {azienda['macroarea']}\n"
        f"- Codice ATECO: {azienda['codice_ateco']}\n"
        f"- Regione: {azienda['regione']}\n"
        f"- Forma giuridica: {azienda.get('forma_giuridica', 'ND')}\n"
        f"- Alcuni indici chiave: {azienda.get('indici', {})}\n\n"
        f"Analizza i seguenti bandi e restituisci solo quelli compatibili, riportando per ognuno tutti i dati utili.\n"
        f"Formato risposta: lista JSON con oggetti bando completi. Nessuna spiegazione testuale, solo JSON.\n\n"
    )
    corpo = ""
    for bando in bandi:
        corpo += json.dumps(bando, ensure_ascii=False) + "\n"
    return intestazione + corpo

def chiama_claude_completo(prompt: str):
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 4000,
        "temperature": 0.3,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = openai._make_http_request("POST", CLAUDE_API_URL, headers=headers, json_data=payload)
    content = response.json()
    testo = content['content'][0]['text']
    try:
        lista_bandi = json.loads(testo)
        return lista_bandi
    except Exception:
        return []

def filtra_bandi_con_claude_completo(nome_view: str, azienda: dict):
    bandi = estrai_bandi_completi(nome_view)
    prompt = costruisci_prompt_completo(bandi, azienda)
    return chiama_claude_completo(prompt)
