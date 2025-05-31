
import imaplib
import email
from email.header import decode_header
import os
import json
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ENV from Render
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GOOGLE_SERVICE_ACCOUNT = os.getenv("GOOGLE_SERVICE_ACCOUNT")

# Google Drive setup
SCOPES = ["https://www.googleapis.com/auth/drive"]
creds_info = json.loads(GOOGLE_SERVICE_ACCOUNT)
creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)

def create_drive_folder(folder_name):
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    logging.info(f"Created folder '{folder_name}' with ID: {folder.get('id')}")
    return folder.get("id")

def upload_to_drive(folder_id, filename, filepath):
    file_metadata = {
        "name": filename,
        "parents": [folder_id]
    }
    media = MediaFileUpload(filepath, mimetype="application/pdf")
    drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    logging.info(f"Uploaded '{filename}' to folder ID: {folder_id}")

def process_emails():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL_SENDER, EMAIL_PASSWORD)
    imap.select("inbox")

    status, messages = imap.search(None, '(UNSEEN)')
    if status != "OK":
        logging.error("No messages found.")
        return

    for num in messages[0].split():
        res, msg_data = imap.fetch(num, "(RFC822)")
        if res != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        azienda = subject.strip()

        logging.info(f"Processing email with subject: {azienda}")

        folder_id = create_drive_folder(azienda)

        for part in msg.walk():
            if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
                continue
            filename = part.get_filename()
            if filename:
                filename = decode_header(filename)[0][0]
                if isinstance(filename, bytes):
                    filename = filename.decode()
                filepath = f"/tmp/{filename}"
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                logging.info(f"Saved attachment: {filepath}")
                upload_to_drive(folder_id, filename, filepath)

    imap.logout()

if __name__ == "__main__":
    process_emails()
