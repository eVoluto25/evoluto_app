# claude_fallback.py – Analisi semantica per top 3 bandi con Claude

import os
import openai
import json

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-opus")

def prepara_prompt_claude(data: dict) -> str:
    azienda = data["azienda"]
    bando = data["bando"]
    score = data.get("score", 0)
    fascia = data.get("fascia", "")
    note = data.get("note", [])

    prompt = f"""Agisci come un esperto di finanza agevolata italiana.

Valuta se il seguente bando pubblico è compatibile con la situazione dell'azienda. Usa una logica simile a quella delle commissioni valutatrici dei bandi regionali e ministeriali.

Fornisci:
- La macroarea effettiva che secondo te descrive l'obiettivo del bando
- Un giudizio sintetico sulla coerenza con la macroarea assegnata all'azienda
- Una previsione della probabilità di ammissione (Alta / Media / Bassa)
- Una motivazione concisa (max 5 righe)
- Parole chiave rilevanti trovate nell'obiettivo del bando

Dati azienda:
- Macroarea attuale: {azienda['macroarea']}
- Codice ATECO: {azienda.get('ateco', 'ND')}
- Regione: {azienda.get('regione', 'ND')}
- Indicatori principali: {json.dumps(azienda.get('indici', {}), indent=2)}

Dati bando:
- Titolo: {bando.get('Titolo')}
- Obiettivo / Finalità: {bando.get('Obiettivo_Finalita')}
- Forma agevolazione: {bando.get('Forma_agevolazione')}
- Regioni: {bando.get('Regioni')}
- Codici ATECO: {bando.get('Codici_ATECO')}

Rispondi in formato JSON con queste chiavi:
- macroarea_validata
- approvazione_probabile
- motivazione
- note_semantiche
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
            temperature=0.3,
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
    output = {
        "macroarea_validata": None,
        "approvazione_probabile": None,
        "motivazione": testo,
        "note_semantiche": "Estratto base Claude"
    }
    lower = testo.lower()

    if "espansione" in lower:
        output["macroarea_validata"] = "Espansione"
    elif "crescita" in lower:
        output["macroarea_validata"] = "Crescita"
    elif "crisi" in lower:
        output["macroarea_validata"] = "Crisi"

    if "alta" in lower:
        output["approvazione_probabile"] = "alta"
    elif "media" in lower:
        output["approvazione_probabile"] = "media"
    elif "bassa" in lower:
        output["approvazione_probabile"] = "bassa"

    return output

def analizza_top_bandi(bandi_top: list, azienda: dict, macroarea: str, indici: dict) -> list:
    risultati = []
    top3 = bandi_top[:3]

    for b in top3:
        dati = {
            "azienda": {
                **azienda,
                "macroarea": macroarea,
                "indici": indici
            },
            "bando": b["Bando"],
            "score": b["Scoring"]["score"],
            "fascia": b["Scoring"]["fascia"],
            "note": b["Scoring"]["note"]
        }
        out = chiama_claude(dati)
        risultati.append({
            "ID": b["ID"],
            "Titolo": b["Titolo"],
            "Score": b["Score"],
            "RispostaClaude": out
        })

    return risultati