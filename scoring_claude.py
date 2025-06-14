
import json
from typing import List, Dict
from openai import OpenAI  # o Anthropic, se Claude è accessibile da lì

client = OpenAI()  # sostituire con client Claude se necessario

def classifica_bandi_claude(bandi: List[Dict], azienda: Dict) -> List[Dict]:
    prompt = f"""
📄 Bandi disponibili (massimo 25):
{bandi}

🎯 Obiettivo:
Scegli solo i 3 bandi più coerenti con la struttura aziendale seguente:
{azienda}

Per ciascuno dei 3 bandi con punteggio ≥80, restituisci:

- "titolo": stringa
- "motivazione": max 300 caratteri
- "spesa_minima_e_contributo": esempio "min 10.000€ - max 50.000€" oppure null
- "percentuale_agevolazione": esempio "50% fondo perduto" oppure null
- "data_scadenza": formato "YYYY-MM-DD" se nota, altrimenti null

📤 Rispondi solo con un JSON così strutturato, ordinato per coerenza decrescente, **senza testo descrittivo**:

{
  "messaggio": "Il sistema eVoluto ha selezionato per te:",
  "bandi": [
    {
      "titolo": "...",
      "motivazione": "...",
      "spesa_minima_e_contributo": "...",
      "percentuale_agevolazione": "...",
      "data_scadenza": "..."
    }
  ]
}
"""

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1500,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        json_response = json.loads(response.content[0].text)
        return json_response.get("bandi", [])
    except Exception:
        return []
