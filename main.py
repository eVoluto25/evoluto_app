from fastapi import FastAPI
from pydantic import BaseModel
import threading
import uuid
import os
import json
import logging
from scoring_bandi import seleziona_bando_migliore

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
        "messaggio": "Richiesta ricevuta, il sistema eVoluto è ora attivo."
    }

def elabora_dati(dati: dict, filepath: str):
    logging.info(f"Avvio analisi per: {dati['azienda']}")

    # ⬇️ Calcolo reale del bando migliore
    bando, diagnostica, forward_to_claude = seleziona_bando_migliore(
        macroarea=dati["macroarea"],
        indici=dati["indici"]
    )

    dati["top_bando"] = bando
    dati["diagnostica"] = diagnostica
    dati["forward_to_claude"] = forward_to_claude

    with open(filepath, "w") as f:
        json.dump(dati, f, indent=2)

    logging.info(f"Elaborazione completata per: {dati['azienda']}")
