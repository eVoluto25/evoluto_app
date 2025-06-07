import logging
import uvicorn
import os
from bilancio import calcola_indici_finanziari  
from macroarea import assegna_macroarea
from bandi_matcher import trova_bandi_compatibili
from valutazione_punteggio import calcola_valutazione
from output_gpt import genera_output_gpt
from pdf_cleaner import pulisci_pdf
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from pipeline import esegui_pipeline as processa_analisi_pdf
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload/")
async def upload(request: Request):
    body = await request.json()
    
    comando = body.get("comando")
    nome_file = body.get("nome_file")
    contenuto = body.get("contenuto")  # deve essere base64 o testo
    logger.info(f"Ricevuto comando: {comando}, file: {nome_file}")

    if comando.strip().lower() != "esegui analisi aziendale":
        logger.warning("Comando non valido.")
        return JSONResponse(content={"errore": "Comando non valido"}, status_code=400)

    try:
        risultato = avvia_analisi_completa(nome_file, contenuto)
        logger.info("Analisi completata.")
        return {"risultato": risultato}
    except Exception as e:
        logger.error(f"Errore durante analisi: {e}")
        return JSONResponse(content={"errore": str(e)}, status_code=500)

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

    except Exception as e:
        logging.error(f"Errore durante il processo: {e}", exc_info=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logging.error("Percorso al file XBRL o PDF mancante.")
    else:
        main(sys.argv[1])
