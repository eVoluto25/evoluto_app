import os
import openai

openai.api_key = os.getenv("OPENAI_KEY")

def analyze_texts_with_gpt(texts):
    if not texts:
        raise ValueError("❌ Nessun testo fornito a GPT.")

    try:
        prompt = f"""Analizza i seguenti testi aziendali e restituisci valutazioni su solidità finanziaria, orientamento alla crescita e possibilità di accesso al credito.

Testi:
{texts}
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        output = response["choices"][0]["message"]["content"]
        return {"analisi": output}

    except Exception as e:
        raise RuntimeError(f"Errore durante la chiamata a GPT: {str(e)}")
