
from googleapiclient.discovery import build
from evoluto_auth import get_google_credentials

SPREADSHEET_ID = "your_spreadsheet_id_here"  # Inserisci il tuo Spreadsheet ID
SHEET_NAME = "Scheda Azienda"

def scrivi_macroarea_in_scheda(sheet, macroarea):
    mappa_righe = {
        "Crisi o Risanamento Aziendale": 42,
        "Crescita e Sviluppo (Start up, PMI, investimenti)": 43,
        "Espansione, Mercati Esteri e Transizione Ecologica": 44
    }

    riga = mappa_righe.get(macroarea)
    if riga:
        range_x = f"B{riga}"
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!{range_x}",
            valueInputOption="RAW",
            body={"values": [["X"]]}
        ).execute()

def write_to_sheets(analisi, azienda):
    creds = get_google_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    valori_base1 = [
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
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!B2:B12",
        valueInputOption="RAW",
        body={"values": [[v] for v in valori_base1]}
    ).execute()

    indici = analisi.get("indici", [])
    valori = [[i.get("valore", ""), i.get("commento", ""), i.get("valutazione", "")] for i in indici]
    range_indici = f"{SHEET_NAME}!B18:D{18 + len(valori) - 1}"
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_indici,
        valueInputOption="RAW",
        body={"values": valori}
    ).execute()

    scrivi_macroarea_in_scheda(sheet, analisi.get("macroarea"))

    return analisi.get("macroarea", "Non definita")
