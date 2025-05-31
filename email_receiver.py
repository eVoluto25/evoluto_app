import imaplib
import email
import os
import logging
import requests
import fitz  # PyMuPDF
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# --- CONFIG ---
EMAIL_HOST = "imap.gmail.com"
EMAIL_PORT = 993
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
API_ENDPOINT = "https://evoluto-app-wa89.onrender.com/process"
CREDENTIALS_FILE = "credentials.json"
DRIVE_FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID")

# --- LOGGING ---
logging.basicConfig(
    filename="email_processor.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- SETUP GOOGLE DRIVE ---
def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=creds)

def crea_cartella_drive(nome_cartella, drive_service):
    file_metadata = {
        'name': nome_cartella,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [DRIVE_FOLDER_ID]
    }
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    logging.info(f"Cartella creata su Drive: {nome_cartella} - ID: {folder['id']}")
    return folder['id']

def carica_file_drive(filepath, folder_id, drive_service):
    nome_file = os.path.basename(filepath)
    media = MediaFileUpload(filepath, mimetype='application/pdf')
    file_metadata = {
        'name': nome_file,
        'parents': [folder_id]
    }
    drive_service.files().create(body=file_metadata, media_body=media).execute()
    logging.info(f"File caricato su Drive: {nome_file}")

# --- FUNZIONI EMAIL ---
def salva_allegati(msg, save_dir):
    filepaths = []
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename and filename.endswith(".pdf"):
            filepath = os.path.join(save_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            logging.info(f"Allegato salvato: {filepath}")
            filepaths.append(filepath)
    return filepaths

def verifica_pdf(filepath):
    try:
        with fitz.open(filepath) as doc:
            text = "".join(page.get_text() for page in doc)
            return len(text.strip()) > 20
    except Exception as e:
        logging.warning(f"PDF non leggibile: {filepath} - {e}")
        return False

def invia_api(nome_azienda, folder_id):
    try:
        payload = {
            "folder_id": folder_id,
            "spreadsheetId": os.environ.get("SHEET_ID"),
            "azienda": {
                "denominazione": nome_azienda
            }
        }
        response = requests.post(API_ENDPOINT, json=payload)
        logging.info(f"Chiamata API: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception("Errore chiamata API")

# --- PROCESSO COMPLETO ---
def processa_email():
    try:
        mail = imaplib.IMAP4_SSL(EMAIL_HOST)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        status, messages = mail.search(None, '(UNSEEN)')
        if status != "OK":
            logging.error("Errore nella ricerca email.")
            return

        for num in messages[0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            subject = email.header.decode_header(msg["Subject"])[0][0]
            subject = subject.decode() if isinstance(subject, bytes) else subject
            logging.info(f"Email ricevuta - Oggetto: {subject}")

            temp_dir = f"emails/{subject}"
            os.makedirs(temp_dir, exist_ok=True)
            filepaths = salva_allegati(msg, temp_dir)
            filepaths = [f for f in filepaths if verifica_pdf(f)]

            if filepaths:
                drive_service = get_drive_service()
                folder_id = crea_cartella_drive(subject, drive_service)
                for file in filepaths:
                    carica_file_drive(file, folder_id, drive_service)
                invia_api(subject, folder_id)

            mail.store(num, '+FLAGS', '\\Seen')

        mail.logout()

    except Exception as e:
        logging.exception("Errore nel processo email")

# --- MAIN ---
if __name__ == "__main__":
    os.makedirs("emails", exist_ok=True)
    processa_email()
