import os
import json
import tempfile
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Config
BASE_FILENAME = "aziende_scraping"
FOLDER_NAME = "Scraping Aziende"

# Crea filename con data odierna
def get_csv_filename():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{BASE_FILENAME}_{today}.csv"

# Carica credenziali da variabile d'ambiente e crea file temporaneo
def get_drive_service():
    scopes = ["https://www.googleapis.com/auth/drive"]
    json_str = os.environ["GOOGLE_DRIVE_CREDENTIALS_JSON"]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp_file:
        temp_file.write(json_str)
        temp_file.flush()
        credentials_path = temp_file.name

    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=scopes
    )
    return build("drive", "v3", credentials=creds)

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

if __name__ == "__main__":
    csv_filename = get_csv_filename()

    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"⚠ Il file {csv_filename} non esiste.")
    
    service = get_drive_service()
    folder_id = get_folder_id(service, FOLDER_NAME)
    upload_file(service, csv_filename, folder_id)
