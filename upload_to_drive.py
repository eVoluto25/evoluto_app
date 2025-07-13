import os
import base64
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Config
BASE_FILENAME = "aziende_scraping"
FOLDER_NAME = "Scraping Aziende"
CREDENTIALS_PATH = "credentials.json"

# Step 1: Decodifica e salva il file delle credenziali dal secret base64
def decode_and_save_credentials():
    creds_b64 = os.environ.get("GOOGLE_DRIVE_CREDENTIALS_JSON")
    if not creds_b64:
        raise ValueError("⚠ Variabile GOOGLE_DRIVE_CREDENTIALS_JSON non trovata.")
    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    with open(CREDENTIALS_PATH, "w") as f:
        f.write(creds_json)

# Step 2: Costruisce filename con la data odierna
def get_csv_filename():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{BASE_FILENAME}_{today}.csv"

# Step 3: Inizializza il servizio Google Drive
def get_drive_service():
    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=scopes
    )
    return build("drive", "v3", credentials=creds)

# Step 4: Recupera o crea la cartella su Google Drive
def get_folder_id(service, folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])
    if folders:
        return folders[0]["id"]
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    return folder.get("id")

# Step 5: Carica il file CSV nella cartella indicata
def upload_file(service, filename, folder_id):
    file_metadata = {
        "name": filename,
        "parents": [folder_id]
    }
    media = MediaFileUpload(filename, resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()
    print(f"✔ File caricato: {uploaded_file.get('id')}")

# MAIN
if __name__ == "__main__":
    decode_and_save_credentials()
    csv_filename = get_csv_filename()

    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"⚠ Il file {csv_filename} non esiste.")

    service = get_drive_service()
    folder_id = get_folder_id(service, FOLDER_NAME)
    upload_file(service, csv_filename, folder_id)
