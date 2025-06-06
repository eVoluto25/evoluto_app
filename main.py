
import logging
from bilancio import calcola_indici_finanziari  
from macroarea import assegna_macroarea
from bandi_matcher import trova_bandi_compatibili
from valutazione_punteggio import calcola_valutazione
from output_gpt import genera_output_gpt
from pdf_cleaner import pulisci_pdf
from fastapi import FastAPI, UploadFile
from pipeline import esegui_pipeline

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile):
    contenuto = await file.read()
    nome_file = file.filename
    with open(nome_file, "wb") as f:
        f.write(contenuto)
    output = esegui_pipeline(nome_file, nome_file)
    return {"risultato": output}

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
