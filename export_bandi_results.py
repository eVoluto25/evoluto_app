from config import get_google_credentials, SPREADSHEET_ID
import gspread

# Costanti
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDENTIALS_PATH = "path/to/credentials.json"
FOGLIO_BANDI = "Bandi"

# Connessione a Google Sheets
def get_sheet():
    creds = get_google_credentials()
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    return sheet.worksheet("Bandi")

# Esporta bandi selezionati nella tabella
def export_bandi_results(bandi):
    MIN_BANDI = 5
    MAX_BANDI = 20

    bandi_ordinati = sorted(bandi, key=lambda x: x.get("punteggio", 0), reverse=True)
    bandi_selezionati = bandi[:MAX_BANDI]
    
    if len(bandi_selezionati) < MIN_BANDI:
        raise ValueError("Non ci sono abbastanza bandi idonei per procedere.")

    sheet = get_sheet()

    # Scrive la somma in A2
    stanziamento = sum(b.get("importo", 0) for b in bandi_selezionati)
    sheet.update("A2", [[stanziamento]])

    # Scrive i bandi da riga 6 in poi, colonne A-H
    for i, bando in enumerate(bandi_selezionati):
        riga = 6 + i
        punteggio = bando.get("punteggio", 0)
        stelle = "⭐️⭐️⭐️⭐️⭐️" if punteggio >= 80 else "⭐️⭐️⭐️" if punteggio >= 50 else "⭐️"
        valori = [
            bando.get("Titolo", ""),
            bando.get("Forma_agevolazione", ""),
            bando.get("Obiettivo_Finalita", ""),
            bando.get("Stanziamento_incentivo", 0),
            bando.get("Data_apertura", ""),
            bando.get("Data_chiusura", ""),
            bando.get("🔸 Punteggio 0 – 100", ""),
            bando.get("🔸 Classificazione qualitativa", "")
        ]
        cella_inizio = f"A{riga}"
        cella_fine = f"H{riga}"
        sheet.update(f"{cella_inizio}:{cella_fine}", [valori])
