import openai
import os

CLAUDE_API_KEY = os.getenv("CLAUDE_KEY")

def match_bandi_with_claude(bandi_filtrati, analisi_azienda):
    import openai

    prompt = f"""Seleziona e valuta i bandi in base ai seguenti criteri.

🎯 1. Criteri di Scoring e Pesi

🔹 A. Compatibilità con la Macro Area – 30%
• Se l’azienda appartiene alla stessa macro area del bando, punteggio pieno.
• Se afferente ma non perfettamente allineata, punteggio parziale.

🔹 B. Solidità Finanziaria – 25%
• Valutazione basata su:
    - EBITDA Margin > 10%
    - Utile netto positivo
    - Debt/Equity tra 0.5 e 2
• Se uno o più indicatori sono critici, penalizzazione progressiva.

🔹 C. Forma dell’agevolazione – 15%
• Fondo perduto: massimo punteggio
• Credito d’imposta: medio
• Finanziamento agevolato: basso

🔹 D. Dimensione Aziendale – 10%
• Se il bando è per PMI e l’azienda è PMI → + punti
• Se mismatch → penalità

🔹 E. Capacità di co-finanziamento / Spesa ammessa – 10%
• Se l’azienda ha capacità di sostenere la spesa ammessa → + punti

🔹 F. Territorio e Settore ATECO – 10%
• Coerenza tra bando e localizzazione / settore aziendale

🧮 Output atteso:
Per ogni bando restituisci un oggetto JSON così strutturato:
[
  {{
    "titolo": "...",
    "agevolazione": "...",
    "obiettivo": "...",
    "apertura": "...",
    "scadenza": "...",
    "punteggio": 87,
    "valutazione": "Alta probabilità di aggiudicazione",
    "importo": 150000
  }},
  ...
]

Bandi da valutare: {bandi_filtrati}
Analisi azienda: {analisi_azienda}
"""

    response = openai.ChatCompletion.create(
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": prompt}],
        api_key=CLAUDE_API_KEY
    )

    import json
    result_text = response.choices[0].message["content"]
    try:
        return json.loads(result_text)
    except Exception:
        return []