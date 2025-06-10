import os
import json
import logging
import email
from email import policy
from email.parser import BytesParser
import imaplib
from fastapi import FastAPI
from pipeline import pipeline as esegui_pipeline

# === CONFIGURAZIONE LOG ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)

app = FastAPI()

@app.post("/ricevi_analisi")
async def ricevi_analisi(dati: dict):
    try:
        filename = dati.get("filename", "analisi_gpt.json")
        content = dati.get("content", "{}")

        # Salvataggio del file JSON ricevuto
        with open(f"/tmp/{filename}", "w") as f:
            f.write(content)

        logging.info(f"✅ JSON ricevuto e salvato come {filename}")
        return {"status": "success", "filename": filename}
    except Exception as e:
        logging.error(f"❌ Errore durante il salvataggio del JSON: {e}")
        return {"status": "error", "message": str(e)}

def main():
    dati_azienda = recupera_json_dal_corpo()
    if dati_azienda:
        logging.info("🚀 Avvio dell'analisi tramite pipeline.")
        risultato = esegui_pipeline(dati_azienda)
        logging.info("📦 Analisi completata. Risultato:")
        logging.info(json.dumps(risultato, indent=2, ensure_ascii=False))
    else:
        logging.info("🛑 Nessun dato disponibile per l’analisi.")

if __name__ == "__main__":
    main()
