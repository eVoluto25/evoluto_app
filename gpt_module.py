import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def build_prompt(azienda_data):
    return f'''
Fornisci un'analisi in JSON dei seguenti dati aziendali, con questi campi:
- autofinanziamento
- disponibilità_liquide
- indebitamento
- solidità_finanziaria
- redditività
- investimenti
- voto_finale
- commento_generale

Dati:
{json.dumps(azienda_data, indent=2)}

Rispondi solo in JSON.
'''

def run_gpt_analysis(azienda_data):
    prompt = build_prompt(azienda_data)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un analista finanziario esperto."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    reply = response['choices'][0]['message']['content']
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        raise ValueError("Errore parsing JSON GPT:\n" + reply)
