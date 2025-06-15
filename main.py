
import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from analisi_finanziaria import calcola_indici, assegna_macro_area, calcola_dimensione
from query_supabase import estrai_bandi
from scoring_claude import classifica_bandi_claude

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class Anagrafica(BaseModel):
    codice_ateco: str
    dipendenti: int
    regione: str

class Bilancio(BaseModel):
    ricavi: Any
    utile_netto: Any
    ebitda: Any
    ebit: Any
    ammortamenti: Any
    oneri_finanziari: Any
    patrimonio_netto: Any
    attivo_corrente: Any
    passivo_corrente: Any
    debiti_totali: Any
    debiti_finanziari: Any
    totale_attivo: Any
    immobilizzazioni: Any
    ricavi_anno_prec: Any
    immobilizzazioni_prec: Any

class AziendaInput(BaseModel):
    anagrafica: Anagrafica
    bilancio: Bilancio

@app.post("/analizza-azienda")
def analizza_azienda(input_data: AziendaInput):

    logger.debug("Calcolo dimensione e indici")
    dimensione = calcola_dimensione(
        int(input_data.anagrafica.dipendenti or 0),
        float(input_data.bilancio.ricavi or 0.0),
        float(input_data.bilancio.totale_attivo or 0.0)
    )

    logger.debug("Pulizia dati di bilancio in corso")
    bilancio_pulito = {}
    chiavi_bilancio = [
        "utile_netto", "ebit", "ebitda", "fatturato",
        "patrimonio_netto", "debiti_totali", "debiti_finanziari",
        "totale_attivo", "attivo_corrente", "passivo_corrente",
        "interessi_passivi", "oneri_finanziari",
        "immobilizzazioni", "immobilizzazioni_prec", "ricavi_anno_prec"
    ]

    for k in chiavi_bilancio:
        raw = input_data.bilancio.__dict__.get(k)
        try:
            bilancio_pulito[k] = float(raw)
        except (TypeError, ValueError):
            logger.warning(f"[{k}] valore assente o non valido: '{raw}', impostato a 0.")
            bilancio_pulito[k] = 0.0

    logger.debug(f"Dati di bilancio puliti: {bilancio_pulito}")

    indici = calcola_indici(bilancio_pulito)
    logger.debug(f"Indici calcolati: {indici}")

    macro_area = assegna_macro_area(indici)
    logger.debug(f"Macro area assegnata: {macro_area}")

    bandi = estrai_bandi(macro_area, dimensione)
    logger.debug(f"Bandi estratti: {bandi[:3]}")

    azienda_data = {
        "regione": input_data.anagrafica.regione,
        "codice_ateco": input_data.anagrafica.codice_ateco,
        "dimensione": dimensione,
        "indici": indici,
    }

    commento = classifica_bandi_claude(bandi, azienda_data)
    logger.debug("Commento Claude generato")

    return {
        "macro_area": macro_area,
        "dimensione": dimensione,
        "z_score": indici.get("Z_Score"),
        "mcc_rating": indici.get("MCC", "N/D"),
        "bandi_raccomandati": commento
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
