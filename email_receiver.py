
import imaplib
import email
from email.header import decode_header
import os
import re
import logging
from datetime import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials


import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.handlers = [handler]

# === VARIABILI ===
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
DRIVE_PARENT_FOLDER_ID = os.getenv("DRIVE_PARENT_FOLDER_ID")

def connect_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        logging.info("📬 Connessione email stabilita")
        print("✅ Connessione email stabilita")
        return mail
    except Exception as e:
        logging.error(f"❌ Errore connessione email: {e}")
        return None

def clean_subject(subject):
    subject = decode_header(subject)[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()
    return re.sub(r"[\W\s]+", "", subject).strip()

def upload_to_drive(folder_name):
    try:
        import json
        with open("client_secrets.json", "w") as f:
            f.write(os.getenv("GOOGLE_SERVICE_ACCOUNT"))
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'service_account.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )

        drive = GoogleDrive(gauth)    

        # Crea la cartella principale per i file
        folder_metadata = {
            'title': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{"id": DRIVE_PARENT_FOLDER_ID}]
        }
        parent_folder = drive.CreateFile(folder_metadata)
        parent_folder.Upload()

        file_list = os.listdir(folder_name)
        for file_name in file_list:
            file_path = os.path.join(folder_name, file_name)
            gfile = drive.CreateFile({
                'title': file_name,
                'parents': [{"id": parent_folder['id']}]
            })
            gfile.SetContentFile(file_path)
            gfile.Upload()

        logging.info(f"📁 Caricamento completato su Drive: {folder_name}")
    except Exception as e:
        logging.error(f"❌ Errore caricamento su Drive: {e}")

def process_emails():
    try:
        mail_server = os.environ.get("EMAIL_SERVER", "imap.gmail.com")
        mail_user = os.environ["EMAIL_USERNAME"]
        mail_pass = os.environ["EMAIL_PASSWORD"]

        logging.info("▶ Avvio connessione email...")

        mail = imaplib.IMAP4_SSL(mail_server)
        mail.login(mail_user, mail_pass)
        mail.select("inbox")

        logging.info(f"✅ Connessione email stabilita con: {mail_user}")

        result, data = mail.search(None, '(UNSEEN)')
        if result != "OK":
            logging.warning("⚠ Impossibile recuperare le email non lette.")
            return

        email_ids = data[0].split()
        logging.info(f"📥 Email non lette trovate: {len(email_ids)}")

        for eid in email_ids:
            res, msg_data = mail.fetch(eid, "(RFC822)")
            if res != "OK":
                logging.warning(f"⚠ Errore nel recupero dell'email ID {eid}")
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get("Subject", "[Senza oggetto]")
            sender = msg.get("From", "[Sconosciuto]")
            logging.info(f"📧 Email da: {sender}, oggetto: {subject}")
            # TODO: aggiungi qui il tuo parsing e logica

    except Exception as e:
        logging.error(f"❌ Errore in process_emails: {str(e)}")
