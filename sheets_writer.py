import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import SPREADSHEET_ID

def get_google_credentials():
    creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT")
    creds_info = json.loads(creds_json)
    return service_account.Credentials.from_service_account_info(creds_info)

def write_to_sheets(dati, azienda, macroarea):
    creds = get_google_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Scrittura dati aziendali
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
    range_base = "B3:B12"
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_base,
        valueInputOption="RAW",
        body={"values": [[v] for v in valori_base]}
    ).execute()

    # Celle fisse per gli indici da B19 in giù (salti riga 25, 26, 34, 35 per spazi e intestazioni)
    celle_valori = [
        "B19", "B20", "B21", "B22", "B23", "B24",
        "B27", "B28", "B29", "B30", "B31", "B32", "B33",
        "B36", "B37"
    ]
    celle_commenti = [c.replace("B", "C") for c in celle_valori]
    celle_valutazioni = [c.replace("B", "D") for c in celle_valori]

    indici = gpt_output.get("indici", [])
    for i, cella in enumerate(celle_valori):
        if i >= len(indici):
            break
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{cella}:{cella}",
            valueInputOption="RAW",
            body={"values": [[indici[i].get("valore", "")]]}
        ).execute()

        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{celle_commenti[i]}:{celle_commenti[i]}",
            valueInputOption="RAW",
            body={"values": [[indici[i].get("commento", "")]]}
        ).execute()

        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{celle_valutazioni[i]}:{celle_valutazioni[i]}",
            valueInputOption="RAW",
            body={"values": [[indici[i].get("valutazione", "")]]}
        ).execute()

    # Scrittura macroarea con ✔️ nelle righe 42, 43, 44
    macroarea = gpt_output.get("macroarea", "Non definita")
    mappa_macro = {
        "🔴 1. Crisi o Risanamento Aziendale": "C42",
        "🟠 2. Crescita e Sviluppo (Start up, PMI, investimenti)": "C43",
        "🟢 3. Espansione, Mercati Esteri e Transizione Ecologica": "C44"
    }

    cella_macro = mappa_macro.get(macroarea)
    if cella_macro:
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{cella_macro}:{cella_macro}",
            valueInputOption="RAW",
            body={"values": [["X"]]}
        ).execute()

    return macroarea
