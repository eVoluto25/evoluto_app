from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uuid
import logging

from pdf_cleaner import pulisci_pdf
from estrazione import estrai_indici, assegna_macroarea
from classificazione_macroarea import popola_verifica_aziendale
from bandi_matcher import matcha_bandi
from output_builder import genera_output_finale

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/analizza_pdf/")
async def analizza_pdf(file: UploadFile = File(...)):
    try:
        logger.info("📥 Ricevuto file PDF da GPT")

        # Step 1: Pulizia PDF
        contenuto_pulito = pulisci_pdf(await file.read())
        logger.info("✅ Pulizia PDF completata")

        # Step 2: GPT riceve il testo pulito, calcola gli indici e li restituisce
        # Qui si simula il dizionario di indici come se fosse la risposta GPT
        # ⚠️ In produzione: GPT deve ricevere il testo pulito e restituire questi indici
        indici_finanziari = estrai_indici(contenuto_pulito)
        logger.info("✅ Indici finanziari calcolati da GPT")

        # Step 3: Assegnazione Macroarea + Scrittura su Supabase
        macroarea = assegna_macroarea(indici_finanziari)
        id_verifica = str(uuid.uuid4())
        popola_verifica_aziendale(id_verifica, indici_finanziari, macroarea)
        logger.info(f"✅ Dati scritti in verifica_aziendale (ID: {id_verifica})")

        # Step 4: Matching bandi (con pesi e logica)
        bandi_compatibili = matcha_bandi(id_verifica, macroarea, indici_finanziari)
        logger.info("✅ Matching bandi completato")

        # Step 5: Generazione output leggibile
        output = genera_output_finale(id_verifica)
        logger.info("✅ Output finale generato")

        return JSONResponse(content=output)

    except Exception as e:
        logger.error(f"❌ Errore nel processo: {e}")
        return JSONResponse(content={"errore": str(e)}, status_code=500)
