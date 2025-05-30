
from config import SPREADSHEET_ID
from googleapiclient.discovery import build
from google.oauth2 import service_account

def write_to_sheets(analisi, azienda):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys/credentials.json'
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Dati anagrafici
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

    # Celle fisse per gli indici da B18 in giù (salti riga 25, 33, 42 per intestazioni)
    celle_valori = [
        "B18", "B19", "B20", "B21", "B22", "B23",
        "B26", "B27", "B28", "B29", "B30", "B31", "B32",
        "B35", "B36"
    ]
    celle_commenti = [c.replace("B", "C") for c in celle_valori]
    celle_valutazioni = [c.replace("B", "D") for c in celle_valori]

    indici = analisi.get("indici", [])
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

    return analisi.get("macroarea", "Non definita")
