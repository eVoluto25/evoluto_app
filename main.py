from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logging_config import setup_logging
from pdf_cleaner import clean_pdf_texts
from gpt_handler import analyze_texts_with_gpt
from claude_matcher import match_bandi_with_claude
from sheets_writer import write_to_sheets
from drive_utils import get_pdfs_from_drive
from pdf_exporter import export_to_pdf
from classificazione_macroarea import assegna_macroarea
from supabase import create_client
from supabase_connector import fetch_bandi
from prefiltraggio_bandi import filtra_bandi_per_macroarea
from export_bandi_results import export_bandi_results
from config import SPREADSHEET_ID
from fastapi import File, UploadFile
from drive_utils import upload_file_to_drive, create_drive_subfolder
import logging
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/stats")
async def get_stats():
    try:
        response = supabase.table("bandi_disponibili").select("Stanziamento_incentivo, Data_chiusura").execute()
        rows = response.data

        from datetime import datetime
        today = datetime.now().date()

        attivi = [r for r in rows if r["Data_chiusura"] and datetime.strptime(r["Data_chiusura"], "%Y-%m-%d").date() >= today]
        totale = sum(r["Stanziamento_incentivo"] for r in attivi if r["Stanziamento_incentivo"] is not None)

        return {
            "incentivi_attivi": len(attivi),
            "totale_importo": totale
        }
    except Exception as e:
        return {"error": str(e)}

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    return await gestisci_upload_pdf(file)

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        return f.read()

@app.post("/process")
async def process(request: Request):
    try:
        data = await request.json()
        folder_id = data["folder_id"]
        azienda = data["azienda"]

        if not folder_id or not azienda:
            return {"error": "folder_id e azienda sono richiesti."}

        logger.info(f"💻 Avviata Verifica Aziendale per società: {azienda}")
        pdfs = get_pdfs_from_drive(folder_id)

        # 📂 Crea sottocartella per l'azienda nel Drive
        folder_id_archivio = create_drive_subfolder(azienda, DRIVE_PARENT_FOLDER_ID)

        for pdf in pdfs:
            upload_file_to_drive(pdf.name, DRIVE_PARENT_FOLDER_ID)
        logger.info(f"📎 Allegati analizzati: {[pdf.name for pdf in pdfs]}")
        logger.info(f"📥 Bilancio scaricato da Cartella {azienda} su Google Drive")
    
        clean_texts = clean_pdf_texts(pdfs)
        logger.info("🧹 Testi PDF puliti e filtrati")
        
        logger.info(f"📤 Invio {len(clean_texts)} testi per analisi finanziaria 🧠 📊")
        gpt_output = analyze_texts_with_gpt("\n\n".join(clean_texts))
        logger.info("studio 💻 ed elaborazione indici 📈 di bilancio")
        logger.info(f"🧠 📊 Analisi Finanziaria AI completata {gpt_output}")
    
        macroarea = assegna_macroarea(gpt_output)
        logger.info(f"📍 Macroarea assegnata a {azienda}: {macroarea}")

        bandi = fetch_bandi()
        logger.info("📡 elenco Bandi ricevuti 🗄️ 📚")
    
        bandi_filtrati = filtra_bandi_per_macroarea(bandi, macroarea)
        logger.info(f"🔍 Filtrati {len(bandi_filtrati)} bandi rilevanti 📊 per la macroarea")
    
        bandi_idonei = match_bandi_with_claude(gpt_output, bandi_filtrati)
        logger.info(f"🤖 ✅ Matching bandi idonei ✅ completato")

        export_bandi_results(bandi_idonei, SPREADSHEET_ID)
        logger.info("📊 ⌨️ Scrittura bandi idonei su foglio Google Sheets completata")

        send_analysis_email(azienda)
        logger.info(f"✅ Processo concluso ed email inviata al Team eVoluto {EMAIL_TO} per: {azienda}")

        return {"status": "completato", "azienda": azienda}
    
    except Exception as e:
        logging.error(f"❌ Errore connessione email: {e}")
        print(f"❌ Errore connessione email: {e}")
        return None
