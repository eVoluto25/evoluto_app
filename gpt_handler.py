import os
import openai

openai.api_key = os.getenv("OPENAI_KEY")

def analyze_texts_with_gpt(texts):
    prompt = f"""Analizza i seguenti testi aziendali e restituisci valutazioni su solidità finanziaria, orientamento alla crescita e possibile macro-area.

Testi:
{texts}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    output = response["choices"][0]["message"]["content"]
    
    # Puoi fare un parsing JSON qui se GPT restituisce dati strutturati
    return {"analisi": output}
