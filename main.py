import logging
import uvicorn
import os
import shutil
import uuid
from bilancio import calcola_indici_finanziari  
from macroarea import assegna_macroarea
from bandi_matcher import trova_bandi_compatibili
from valutazione_punteggio import calcola_valutazione
from output_gpt import genera_output_gpt
from pdf_cleaner import estrai_testo_pymupdf
from estrazione import esegui_pipeline_intermediario as esegui_pipeline
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from pipeline import esegui_pipeline as processa_analisi_pdf
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="eVoluto API",
    description="API per analisi aziendale, assegnazione macroarea e selezione bandi.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oppure specifica dominio GPT
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ricevi_file")
async def ricevi_file_da_make(request: Request):
    try:
        file_bytes = await request.body()

        # Salva per debug
        with open("/tmp/file_make.pdf", "wb") as f:
            f.write(file_bytes)
        
        logging.info("📥 File ricevuto da Make, avvio pipeline")
        output = esegui_pipeline("file_make.pdf", "/tmp/file_make.pdf")
        
        return {"risultato": output}

    except Exception as e:
        logging.error(f"❌ Errore ricezione file da Make: {str(e)}")
        raise HTTPException(status_code=400, detail="Errore nella ricezione del file")

# Avvio manuale da terminale se necessario
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logging.error("❌ Percorso al file XBRL o PDF mancante.")
    else:
        main(sys.argv[1])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

def main(percorso_file):
    try:
        logging.info("Inizio processo di analisi completa")

        logging.info("Estrazione dati dal file PDF o XBRL")
        testo_estratto, nome_azienda = estrai_dati_da_file(percorso_file)

        logging.info("Calcolo indici di bilancio")
        id_azienda = calcola_indici_bilancio(testo_estratto, nome_azienda)

        logging.info("Assegnazione macroarea")
        assegna_macroarea(id_azienda)

        logging.info("Matching con i bandi disponibili")
        match_bandi(id_azienda)

        logging.info("Calcolo ranking bandi")
        calcola_ranking(id_azienda)

        logging.info("Generazione output GPT")
        genera_output_gpt(id_azienda)

        logging.info("Processo completato con successo")

        with open(nome_file, "wb") as f:
            f.write(contenuto)
            
        output = esegui_pipeline(nome_file, nome_file)
        return {"risultato": output}

    except Exception as e:
        logging.error(f"Errore nel caricamento: {str(e)}")
        raise HTTPException(status_code=400, detail="Errore nel file")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logging.error("Percorso al file XBRL o PDF mancante.")
    else:
        main(sys.argv[1])
