# -*- coding: utf-8 -*-
import requests
import pandas as pd
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# -------------------------
# CONFIGURAZIONE SUPABASE
# -------------------------
SUPABASE_URL = "https://TUA-URL.supabase.co"
SUPABASE_API_KEY = "SUPABASE_API_KEY"
SUPABASE_TABLE = "calendar_tokens"  # o "drive_tokens" se ne usi una dedicata

# 📁 Cartella fissa su Drive
FOLDER_ID = "1bR24tO5767YsmCfQUzUf4mLMcG-vrEzk"

# -------------------------
# LEGGI TOKEN DA SUPABASE
# -------------------------
def recupera_token_da_supabase():
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?select=*&limit=1"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Errore nel recupero token da Supabase")
    return response.json()[0]

# -------------------------
# UPLOAD CSV SU GOOGLE DRIVE
# -------------------------
def upload_to_drive(local_file_path, nome_file_drive, token_data):
    scopes = ["https://www.googleapis.com/auth/drive.file"]
    creds = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=scopes
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    service = build("drive", "v3", credentials=creds)
    file_metadata = {
        "name": nome_file_drive,
        "parents": [FOLDER_ID]
    }
    media = MediaFileUpload(local_file_path, mimetype="text/csv")
    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"✅ Caricato: {nome_file_drive} → ID: {uploaded.get('id')}")

# -------------------------
# ESECUZIONE COMPLETA
# -------------------------
def main():
    oggi = datetime.now().strftime("%Y-%m-%d")
    nome_file_csv = f"aziende_filtrate_{oggi}.csv"

    # 👇 Esempio: lista dummy da sostituire con scraping reale
    df = pd.DataFrame([
        {"ragione_sociale": "Azienda Demo", "email": "demo@azienda.it", "regione": "Lazio"}
    ])
    df.to_csv(nome_file_csv, index=False, encoding="utf-8-sig")

    token_data = recupera_token_da_supabase()
    upload_to_drive(nome_file_csv, nome_file_csv, token_data)

if __name__ == "__main__":
    main()
