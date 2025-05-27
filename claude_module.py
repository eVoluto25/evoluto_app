import os
import anthropic
import json

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def build_prompt_claude(azienda_data, gpt_data, bandi_testo):
    return f'''
Dati aziendali:
{json.dumps(azienda_data, indent=2)}

Analisi GPT:
{json.dumps(gpt_data, indent=2)}

Bandi disponibili:
{bandi_testo}

Genera un JSON con:
- bandi_compatibili: lista con {{titolo, score, motivazione}}
- criteri_compatibilità: {{dimensione, settore, sede, finalità, agevolazione}}
- commento_generale

Rispondi solo in JSON.
'''

def match_with_bandi(azienda_data, gpt_data, bandi_testo):
    prompt = build_prompt_claude(azienda_data, gpt_data, bandi_testo)

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=2000,
        temperature=0.5,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.content[0].text
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Errore parsing JSON Claude:\n" + content)
