# claude_fallback.py – invio dati a Claude per validazione semantica + predizione

import os
import openai  # se usi Claude via OpenAI compatibile oppure sostituire con SDK reale
import json

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")  # da Render
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-opus")

def prepara_prompt_claude(data: dict) -> str:
    azienda = data["azienda"]
    bando = data["bando"]
    score = data.get("score", 0)
    fascia = data.get("fascia", "")
    note = data.get("note", [])

    prompt = f"""Sei un esperto in finanza agevolata. Valuta se il seguente bando è coerente con la situazione aziendale e assegna una probabilità di approvazione.

Macroarea azienda: {azienda['macroarea']}
Regione: {azienda.get('regione', 'ND')}
Codice ATECO: {azienda.get('ateco', 'ND')}
Indicatori finanziari: {json.dumps(azienda.get('indici', {}), indent=2)}

Score tecnico: {score} ({fascia})
Note analisi: {note}

Dati bando:
Titolo: {bando.get('Titolo')}
Obiettivo: {bando.get('Obiettivo_Finalita')}
Forma: {bando.get('Forma_agevolazione')}
Regioni: {bando.get('Regioni')}
Codici ATECO: {bando.get('Codici_ATECO')}
Scadenza: {bando.get('Data_chiusura')}

Fornisci:
- Macroarea corretta (1 parola)
- Probabilità approvazione (alta/media/bassa)
- Motivazione sintetica
- Parole chiave rilevanti rilevate
"""
    return prompt

def chiama_claude(data: dict) -> dict:
    prompt = prepara_prompt_claude(data)

    try:
        response = openai.ChatCompletion.create(
            model=CLAUDE_MODEL,
            api_key=CLAUDE_API_KEY,
            messages=[
                {"role": "system", "content": "Agisci come esperto di bandi pubblici italiani."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )
        testo = response.choices[0].message["content"]

        return {
            "claude_output_raw": testo,
            "claude_parsed": parse_output_claude(testo)
        }

    except Exception as e:
        return {
            "errore": str(e),
            "claude_output_raw": None,
            "claude_parsed": None
        }

def parse_output_claude(testo: str) -> dict:
    # Estrazione base da testo in linguaggio naturale
    output = {
        "macroarea_validata": None,
        "approvazione_probabile": None,
        "motivazione": None,
        "note_semantiche": None
    }
    testo_lower = testo.lower()

    if "espansione" in testo_lower: output["macroarea_validata"] = "Espansione"
    elif "crescita" in testo_lower: output["macroarea_validata"] = "Crescita"
    elif "crisi" in testo_lower: output["macroarea_validata"] = "Crisi"

    if "alta" in testo_lower: output["approvazione_probabile"] = "alta"
    elif "media" in testo_lower: output["approvazione_probabile"] = "media"
    elif "bassa" in testo_lower: output["approvazione_probabile"] = "bassa"

    output["motivazione"] = testo
    output["note_semantiche"] = "Autoestratto Claude – parsing base"

    return output