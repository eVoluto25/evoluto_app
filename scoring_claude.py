from typing import List, Dict
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("CLAUDE_KEY"))

def classifica_bandi_claude(bandi: List[Dict], azienda: Dict) -> str:
    prompt = f"""
Hai a disposizione un elenco di bandi pubblici e i dati di una azienda. Analizza i dati e assegna un punteggio da 0 a 100 a ciascun bando secondo i seguenti criteri:

Criteri di scoring:
1. Compatibilità con la macro-area aziendale [{azienda['macro_area']}] (peso 30%)
2. Solidità finanziaria secondo gli indici forniti (peso 25%)
3. Forma di agevolazione preferibile (fondo perduto > garanzia > prestito) (peso 15%)
4. Coerenza con la dimensione aziendale [{azienda['dimensione']}] (peso 10%)
5. Capacita' di co-finanziamento basata su MCC/Z-Score (peso 10%)
6. Coerenza territoriale e ATECO con azienda [{azienda['regione']}, {azienda['codice_ateco']}] (peso 10%)

I dati aziendali sono:
Regione: {azienda['regione']}
Codice ATECO: {azienda['codice_ateco']}
Dimensione: {azienda['dimensione']}
Macro-area: {azienda['macro_area']}
Z-Score: {azienda['indici'].get('Z_Score', 'N/D')}
MCC: {azienda['indici'].get('MCC', 'N/D')}

---
Bandi disponibili (max 25):
{bandi}

✨ Obiettivo:
Scegli solo i 3 bandi più coerenti con la struttura aziendale.
Per ciascuno:
**Per ogni bando con punteggio ≥80**, restituisci:
- Titolo
- Motivazione sintetica (max 300 caratteri per ciascun bando selezionato)
- Spesa minima richiesta e contributo massimo concesso (se noti)
- Percentuale di agevolazione (fondo perduto o altra forma)
- Data di scadenza (se nota)

Rispondi in formato JSON strutturato come segue:
{
  "macro_area": "...",
  "dimensione": "...",
  "z_score": ...,
  "mcc_rating": ...,
  "bandi_raccomandati": [
    {
      "titolo": "...",
      "motivazione": "...",
      "spesa_minima": "...",
      "agevolazione": "...",
      "scadenza": "..."
    },
    ...max 3...
  ]
}
La prima frase del JSON deve essere: "il sistema eVoluto ha selezionato per te:"
"""

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text if response.content else "Errore nella risposta di Claude."
