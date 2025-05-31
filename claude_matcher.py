import anthropic
import os
import json

client = anthropic.Anthropic(
    api_key=os.getenv("CLAUDE_KEY")
)

def match_bandi_with_claude(analisi_gpt, bandi_filtrati):
    prompt = f"""
Hai a disposizione:
- Un elenco di bandi già filtrati per macroarea
- Un’analisi finanziaria dettagliata dell’azienda

Il tuo compito è associare ad ogni bando un punteggio da 0 a 100, basato su:

🎯 Criteri:
A. Compatibilità con la Macro Area – 30%
B. Solidità Finanziaria (EBITDA, utile, debito) – 25%
C. Forma dell’agevolazione (fondo perduto > credito d’imposta > prestito) – 15%
D. Dimensione aziendale (PMI, startup) – 10%
E. Capacità di co-finanziamento – 10%
F. Coerenza con territorio e ATECO – 10%

🎯 Output:
Rispondi solo con una lista di dizionari JSON, ognuno con:
– titolo (nome_bando)
– agevolazione
– obiettivo
– apertura
– scadenza
– punteggio (0–100)
– valutazione (in stelle: 1, 3 o 5)

Classifica i bandi in ordine decrescente di punteggio. Inserisci solo quelli con punteggio ≥ 50. Min. 5, Max 20.

Analisi azienda:
{analisi_gpt}

Bandi filtrati:
{bandi_filtrati}
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4096,
        temperature=0.4,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    try:
        return json.loads(response.content[0].text)
    except Exception as e:
        print("Errore nella conversione JSON:", e)
        return []
