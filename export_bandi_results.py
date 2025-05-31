from config import get_google_credentials
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
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Bandi")
    return sheet.worksheet("Bandi")

# Esporta bandi selezionati nella tabella
def export_bandi_results(bandi, spreadsheet_id):
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

    # === Calcoli per le colonne dei grafici ===
    forma_agevolazione = [b.get("Forma_agevolazione", "") for b in bandi_selezionati]
    spesa_ammessa_min = [b.get("Spesa_Ammessa_min", 0) for b in bandi_selezionati]
    agevolazione_max = [b.get("Agevolazione_Concedibile_max", 0) for b in bandi_selezionati]
    stanziamento_totale = [b.get("Stanziamento_incentivo", 0) for b in bandi_selezionati]
    data_chiusura = [b.get("Data_chiusura", "") for b in bandi_selezionati]

    # Scrittura su colonne B33:F33
    sheet.update("A31", [[Forma_agevolazione[0]]])
    sheet.update("B31", [[Spesa_ammessa_min[0]]])
    sheet.update("C31", [[Agevolazione_Concedibile_max[0]]])
    sheet.update("D31", [[Stanziamento_incentivo[0]]])
    sheet.update("E31", [[Data_chiusura[0]]])

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
