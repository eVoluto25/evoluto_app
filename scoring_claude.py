import os
import anthropic
from typing import List, Dict

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))

def classifica_bandi_claude(bandi: List[Dict], azienda: Dict) -> str:
    prompt = f"""
Sei un analista esperto di finanza agevolata.

Analizza i bandi forniti alla luce della struttura economico-finanziaria dell’azienda e seleziona i 3 più adatti, motivando brevemente la scelta.

🧾 Dati azienda:
- Regione: {azienda['regione']}
- Codice ATECO: {azienda['codice_ateco']}
- Dimensione: {azienda['dimensione']}
- Macro-area assegnata: {azienda['macro_area']}
- EBITDA Margin: {azienda['indici'].get('EBITDA_margin', 'N/A')}
- Utile netto: {azienda['indici'].get('utile_netto', 'N/A')}
- Debt/Equity: {azienda['indici'].get('Debt_Equity', 'N/A')}

📄 Bandi disponibili (max 25):
{bandi}

🎯 Obiettivo:
Scegli solo i 3 bandi più coerenti con la struttura aziendale.
Per ciascuno:
**Per ogni bando con punteggio ≥80**, restituisci:
- Titolo
- Motivazione sintetica (max 200 caratteri per ciascun bando selezionato)
- Spesa minima richiesta e contributo massimo concesso (se noti)
- Percentuale di agevolazione (fondo perduto o altra forma)
- Data di scadenza (se nota)

Rispondi in formato JSON con una lista ordinata decrescente in formato elenco numerato e metti come prima frase: "il sistema eVoluto ha selezionato per te:"
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
