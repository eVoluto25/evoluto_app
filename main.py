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
async def ricevi_file(request: Request):
    body = await request.json()
    filename = body.get("filename")
    content = body.get("content")

    try:
        dati_azienda = json.loads(content)
        azienda_id = dati_azienda.get("ragione_sociale", "X")
        email_destinatario = "info@capitaleaziendale.it"
        pipeline(dati_azienda, azienda_id, email_destinatario)
        return {"status": "ok", "message": "Analisi avviata"}
    except Exception as e:
        return {"status": "errore", "message": str(e)}

def recupera_json_dal_corpo():
    try:
        conn = imaplib.IMAP4_SSL(IMAP_SERVER)
        conn.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        conn.select(IMAP_FOLDER)
        logging.info("📬 Connessione IMAP riuscita.")

        result, data = conn.search(None, 'UNSEEN')
        if result != 'OK' or not data[0]:
            logging.warning("📭 Nessuna email non letta trovata.")
            return None

        for num in data[0].split():
            result, msg_data = conn.fetch(num, '(RFC822)')
            if result != 'OK':
                continue

            msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])
            corpo = msg.get_body(preferencelist=('plain')).get_content()

            try:
                dati = json.loads(corpo)
                logging.info("✅ JSON correttamente estratto dal corpo dell’email.")
                return dati
            except json.JSONDecodeError:
                logging.warning("⚠️ Email trovata, ma il corpo non è un JSON valido.")
                continue

        logging.error("❌ Nessuna email con JSON valido.")
        return None

    except Exception as e:
        logging.error(f"Errore nella connessione IMAP: {e}")
        return None

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
