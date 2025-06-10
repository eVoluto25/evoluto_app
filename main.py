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

# === VARIABILI AMBIENTE (Render) ===
EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
IMAP_SERVER = 'imap.gmail.com'
IMAP_FOLDER = 'INBOX'

app = FastAPI()

@app.post("/ricevi_file")
async def ricevi_analisi(request: Request):
    body = await request.json()
    filename = dati.get("filename")
    content = dati.get("content")

    # Esegui l'analisi Python
    with open(f"/tmp/{filename}", "w") as f:
        f.write(contenuto)

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
