from fastapi import FastAPI, Request
from pdf_cleaner import clean_pdf_texts
from gpt_handler import analyze_texts_with_gpt
from claude_matcher import match_bandi_with_claude
from sheets_writer import write_to_sheets
from drive_utils import get_pdfs_from_drive
from pdf_exporter import export_to_pdf
from classificazione_macroarea import assegna_macroarea
from supabase_connector import fetch_bandi
from prefiltraggio_bandi import filtra_bandi_per_macroarea
from export_bandi_results import export_bandi_results

app = FastAPI()

@app.post("/process")
async def process(request: Request):
    data = await request.json()
    folder_id = data["folder_id"]
    azienda = data["azienda"]

    pdfs = get_pdfs_from_drive(folder_id)
    clean_texts = clean_pdf_texts(pdfs)
    gpt_output = analyze_texts_with_gpt(clean_texts)
    
    macroarea = classifica_macro_area(gpt_output)
    bandi = fetch_bandi()
    bandi_filtrati = filtra_bandi_per_macroarea(bandi, macroarea)
    
    write_to_sheets(gpt_output, azienda, macroarea)
    
    bandi = match_bandi_with_claude(gpt_output, bandi_filtrati)

    return {"status": "completato", "azienda": azienda}
