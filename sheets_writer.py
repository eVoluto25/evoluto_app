
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Autenticazione con Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("GOOGLE_SERVICE_ACCOUNT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
    "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("GOOGLE_CERT_URL", "")
}

credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

# ID del foglio Google da aggiornare
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")

def write_to_sheets(analisi, azienda):
    sheet = service.spreadsheets()

    valori_base = [
        azienda.get("denominazione", ""),
        azienda.get("forma_giuridica", ""),
        azienda.get("codice_ateco", ""),
        azienda.get("partita_iva", ""),
        azienda.get("anno_fondazione", ""),
        azienda.get("dipendenti", ""),
        azienda.get("attivita_prevalente", ""),
        azienda.get("provincia", ""),
        azienda.get("citta", ""),
        azienda.get("amministratore", "")
    ]
    range_base = "B2:B11"
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_base,
        valueInputOption="RAW",
        body={"values": [[v] for v in valori_base]}
    ).execute()

    # Scrittura indici
    indici = analisi.get("indici", [])
    valori = [[i.get("valore", ""), i.get("commento", "")] for i in indici]
    range_indici = "B17:C" + str(17 + len(valori) - 1)
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_indici,
        valueInputOption="RAW",
        body={"values": valori}
    ).execute()

    return analisi.get("macroarea", "Non definita")
