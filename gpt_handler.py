import logging
import os
import openai
import textwrap

logger = logging.getLogger(__name__)
openai.api_key = os.getenv("OPENAI_KEY")

def chunk_text(text, max_len=3500):
    """Divide il testo in blocchi senza spezzare le frasi."""
    return textwrap.wrap(text, width=max_len, break_long_words=False, break_on_hyphens=False)

def load_prompt_template():
    path = os.path.join(os.path.dirname(__file__), "prompt_gpt.txt")
    with open(path, "r") as f:
        return f.read()
    
def analyze_texts_with_gpt(texts):
    if not texts:
        logger.warning("⚠️ Nessun testo fornito a GPT.")
        raise ValueError("❌ Nessun testo fornito")

    prompt_template = load_prompt_template()
    chunks = chunk_text(texts)
    logger.info(f"🧩 Testo diviso in {len(chunks)} blocchi per analisi GPT")

    results = []

    for i, chunk in enumerate(chunks, 1):
        prompt = prompt_template.replace("{text}", chunk)
        try:
            logger.info(f"🔎 Invio blocco {i} a GPT - lunghezza: {len(chunk)} caratteri")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            output = response["choices"][0]["message"]["content"]
            results.append(f"🧾 Blocco {i}:\n{output.strip()}")
        except Exception as e:
            logger.error(f"❌ Errore GPT su blocco {i}: {str(e)}")
            results.append(f"[Errore nel blocco {i}: {e}]")

    logger.info("✅ Analisi GPT completata")
    return {"analisi": "\n\n".join(results)}
