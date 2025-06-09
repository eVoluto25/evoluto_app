import imaplib
import email
import logging
import json

def recupera_email_con_dati(host, username, password):
    logging.info("✉️ Connessione al server email in corso...")
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")

    status, messages = mail.search(None, '(SUBJECT "Analisi GPT - Dati azienda")')
    email_ids = messages[0].split()
    if not email_ids:
        logging.info("⚠️ Nessuna email trovata con oggetto previsto.")
        return None, None

    ultima_email_id = email_ids[-1]
    status, msg_data = mail.fetch(ultima_email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    message = email.message_from_bytes(raw_email)

    for part in message.walk():
        if part.get_content_type() == "text/plain":
            corpo_email = part.get_payload(decode=True).decode()
            try:
                dati_json = json.loads(corpo_email)
                logging.info("
