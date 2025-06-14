from fastapi import FastAPI, Request
from pydantic import BaseModel
import threading
import uuid
import os
import json
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

OUTPUT_DIR = "./elaborazioni"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class AziendaInput(BaseModel):
    azienda: str
    macroarea: str
    indici: dict

@app.post("/analizza")
async def ricevi_dati(dati: AziendaInput):
    elaborazione_id = str(uuid.uuid4())
    filepath = os.path.join(OUTPUT_DIR, f"{elaborazione_id}.json")

    threading.Thread(target=elabora_dati, args=(dati.dict(), filepath)).start()

    return {
        "status": "Elaborazione in corso",
        "id_elaborazione": elaborazione_id,
        "messaggio": "Attendere elaborazione completa per risultato finale"
    }

def elabora_dati(dati: dict, filepath: str):
    logging.info(f"Avvio analisi per: {dati['azienda']}")
    dati["top_bando"] = {
        "id": "BANDO123",
        "score": 92,
        "motivazione": "Coerenza con macroarea e solidità finanziaria"
    }
    with open(filepath, "w") as f:
        json.dump(dati, f, indent=2)
    logging.info(f"Elaborazione completata: {filepath}")
