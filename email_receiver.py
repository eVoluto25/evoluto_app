
import imaplib
import email
from email.header import decode_header
import os
import re
import logging
from datetime import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.handlers = [handler]

# === VARIABILI ===
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"
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
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
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

def process_emails(mail):
    try:
        logger.info("✅ Entrato in process_emails")
        if mail is None:
            print("❌ Connessione email fallita")
            return
        print("✅ Connessione email riuscita")
        
        _, messages = mail.search(None, "UNSEEN")
        logger.info(f"📨 Email non lette trovate: {len(messages[0].split())}")
        
        messages = messages[0].split()

        for num in messages:
            _, msg_data = mail.fetch(num, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = clean_subject(msg["Subject"])
            logging.info(f"📨 Oggetto email: {subject}")
            folder_name = f"{subject}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            os.makedirs(folder_name, exist_ok=True)

            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue

                filename = part.get_filename()
                if filename:
                    file_path = os.path.join(folder_name, filename)
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    logging.info(f"📎 Allegato salvato: {file_path}")

            upload_to_drive(folder_name)
    except Exception as e:
        logging.error(f"❌ Errore elaborazione email: {e}")
