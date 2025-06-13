# app.py

import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
from analisi_indici_macroarea import analizza_macroarea
from matching_bandi import match_bando
from scoring_bandi import calcola_score
import uvicorn

logging.basicConfig(level=logging.INFO)
app = FastAPI()

class AziendaInput(BaseModel):
    anagrafica: dict
    bilancio: dict

class BandoInput(BaseModel):
    bando: dict

@app.post("/analizza")
def analizza(input: AziendaInput):
    dati = {**input.anagrafica, **input.bilancio}
    result = analizza_macroarea(dati)
    return result

@app.post("/match")
def match(input: Request):
    payload = await input.json()
    azienda = payload.get("azienda")
    bando = payload.get("bando")
    return match_bando(azienda, bando)

@app.post("/score")
def score(input: Request):
    payload = await input.json()
    azienda = payload.get("azienda")
    bando = payload.get("bando")
    azienda.update(match_bando(azienda, bando))
    azienda.update(analizza_macroarea({**azienda.get("anagrafica", {}), **azienda.get("bilancio", {})}))
    return calcola_score(bando, azienda)

@app.get("/")
def root():
    return {"status": "eVoluto backend pronto"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
