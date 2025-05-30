import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"

# Connessione a Google Sheets
def get_sheet():
    creds = Credentials.from_service_account_file("path/to/credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    return sheet.worksheet("Bandi")

# Esporta bandi selezionati nella tabella
def export_bandi_results(bandi):
    MIN_BANDI = 3
    MAX_BANDI = 10

    bandi_selezionati = bandi[:MAX_BANDI]
    if len(bandi_selezionati) < MIN_BANDI:
        raise ValueError("Non ci sono abbastanza bandi idonei per procedere.")

    sheet = get_sheet()

    # Scrive la somma in A2
    stanziamento = sum(b.get("importo", 0) for b in bandi_selezionati)
    sheet.update("A2", [[stanziamento]])

    # Scrive i bandi da riga 6 in poi, colonne A-G
    for i, bando in enumerate(bandi_selezionati):
        riga = 6 + i
        valori = [
            bando.get("titolo", ""),
            bando.get("agevolazione", ""),
            bando.get("obiettivo", ""),
            bando.get("apertura", ""),
            bando.get("scadenza", ""),
            bando.get("punteggio", ""),
            bando.get("classificazione", "")
        ]
        cell_range = f"A{riga}:G{riga}"
        sheet.update(cell_range, [valori])
