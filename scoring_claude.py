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
- Indica il titolo del bando
- Dai una motivazione sintetica (max 3 righe)
- Classifica qualitativamente: Alta ✅, Media ⚠️, Bassa ❌

Scarta gli altri. Rispondi in formato elenco numerato e metti come prima frase: "il sistema eVoluto ha selezionato per te:"
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
