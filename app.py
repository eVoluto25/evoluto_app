# app.py

import logging
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
from analisi_indici_macroarea import analizza_macroarea
from matching_bandi import match_bando
from scoring_bandi import calcola_score
from claude_fallback import invia_a_claude
from supabase_client import inserisci_diagnosi, recupera_bando
from gpt_estrattore import estrai_dati_pdf

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_TABELLA = "bandi_semplificata"

class AziendaInput(BaseModel):
    anagrafica: dict
    bilancio: dict

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name
    estratto = estrai_dati_pdf(path)
    return estratto

@app.post("/analizza")
async def analizza(input: AziendaInput):
    dati = {**input.anagrafica, **input.bilancio}
    return analizza_macroarea(dati)

@app.post("/score")
async def score(request: Request):
    payload = await request.json()
    azienda = payload.get("azienda")
    id_bando = payload.get("id_bando")

    if not azienda or not id_bando:
        return {"errore": "Parametri azienda o id_bando mancanti"}

    bando = recupera_bando(SUPABASE_TABELLA, id_bando)
    if not bando:
        return {"errore": f"Bando {id_bando} non trovato"}

    # Pipeline
    azienda.update(analizza_macroarea({**azienda.get("anagrafica", {}), **azienda.get("bilancio", {})}))
    azienda.update(match_bando(azienda, bando))
    risultato = calcola_score(bando, azienda)

    # Claude fallback se necessario
    if risultato["forward_to_claude"]:
        payload_claude = {
            "azienda": azienda,
            "bando": bando,
            "score": risultato
        }
        claude_output = invia_a_claude(payload_claude)
        risultato["macroarea_validata_claude"] = claude_output.get("macroarea_validata")
        risultato["motivazione_claude"] = claude_output.get("motivazione")

    # Salvataggio su Supabase
    record = {
        "azienda_id": azienda.get("anagrafica", {}).get("codice_fiscale"),
        "bando_id": id_bando,
        "score": risultato.get("score"),
        "macroarea": azienda.get("macroarea_primaria"),
        "diagnostica": risultato,
    }
    inserisci_diagnosi(SUPABASE_TABELLA, record)

    return risultato

@app.get("/")
def health():
    return {"status": "eVoluto API attiva"}