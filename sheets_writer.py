
from googleapiclient.discovery import build
from evoluto_auth import get_google_credentials

SPREADSHEET_ID = "your_spreadsheet_id_here"
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

    # Dati identificativi da B3 a B12
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
        range=f"{SHEET_NAME}!B3:B12",
        valueInputOption="RAW",
        body={"values": [[v] for v in valori_base1]}
    ).execute()

    # Indicatori da B18 in poi
    celle_indici = {
        "Fatturato annuo": 18,
        "Totale attivo di bilancio": 19,
        "Patrimonio netto": 20,
        "Utile d’esercizio": 21,
        "EBITDA margin": 22,
        "Current ratio": 23,
        "Debt/equity ratio": 24,
        "Interest coverage ratio": 25,
        "Indice di solidità patrimoniale": 26,
        "Indice di incidenza degli investimenti": 27,
        "Indice di autofinanziamento": 28,
        "Variazione immobilizzazioni": 29,
        "ROS": 30,
        "Crescita fatturato": 31
    }

    for indice in analisi.get("indici", []):
        nome = indice.get("nome")
        if nome in celle_indici:
            riga = celle_indici[nome]
            valori = [[
                indice.get("valore", ""),
                indice.get("commento", ""),
                indice.get("valutazione", "")
            ]]
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{SHEET_NAME}!B{riga}:D{riga}",
                valueInputOption="RAW",
                body={"values": valori}
            ).execute()

    # Capacità di autofinanziamento e investimenti recenti
    altri = [
        azienda.get("autofinanziamento", ""),
        azienda.get("investimenti_recenti", "")
    ]
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!B34:B35",
        valueInputOption="RAW",
        body={"values": [[v] for v in altri]}
    ).execute()

    # Macroarea
    scrivi_macroarea_in_scheda(sheet, analisi.get("macroarea"))
    return analisi.get("macroarea", "Non definita")
