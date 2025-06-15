from typing import List, Dict
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("CLAUDE_KEY"))

def classifica_bandi_claude(bandi: List[Dict], azienda: Dict) -> str:
    prompt = f"""
Hai a disposizione un elenco di bandi pubblici e i dati di una azienda. Analizza i dati e assegna un punteggio da 0 a 100 a ciascun bando secondo i seguenti criteri:

Criteri di scoring:
1. Solidità finanziaria (peso 40%)
   - EBITDA Margin > 10% → + punti
   - Utile netto positivo → + punti
   - Debt/Equity tra 0.5 e 2 → + punti
   - Z-Score e MCC (se critici) → penalizzazione

2. Forma dell’agevolazione (peso 20%)
   - Fondo perduto: massimo
   - Credito d’imposta: medio
   - Finanziamento agevolato: basso

3. Dimensione aziendale (peso 15%)
   - Match perfetto → massimo punteggio
   - Mismatch → penalità

4. Capacità di co-finanziamento (peso 15%)
   - Basata su MCC, Z-Score e utile netto

5. Coerenza economica bando/azienda (peso 10%)
   - Analizza spesa minima e contributo in relazione alla struttura aziendale

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

🎯 Obiettivo:
Scegli solo i 3 bandi più coerenti con la struttura aziendale tra quelli **con punteggii ≥80**
Per ciascuno dei 3 restituisci::
- Titolo
- Obiettivo e finalità dell'incentivo
- Motivazione sintetica (max 150 caratteri per ciascun bando selezionato)
- Spesa minima richiesta e contributo massimo concesso (se noti)
- Percentuale e tipo di agevolazione (fondo perduto o altra forma)
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
