import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any
from analisi_finanziaria import calcola_indici, assegna_macro_area, calcola_dimensione
from query_supabase import estrai_bandi
from scoring_claude import classifica_bandi_claude
import os

app = FastAPI()

class AziendaInput(BaseModel):
    anagrafica: Dict[str, Any]
    bilancio: Dict[str, Any]

@app.post("/analizza-azienda")
def analizza_azienda(input_data: AziendaInput):
    logger.debug(f'Input ricevuto: {input_data}')
    try:
        # Calcolo dimensione e indici
        dimensione = calcola_dimensione(
            int(input_data.anagrafica.get("dipendenti", 0)),
            float(input_data.bilancio.get("ricavi", 0.0)),
            float(input_data.bilancio.get("totale_attivo", 0.0))
        )

        logger.debug('Pulizia dati di bilancio in corso')
    bilancio_pulito = {
            k: float(input_data.bilancio.get(k, 0.0)) for k in [
                "utile_netto", "ebit", "ebitda", "fatturato",
                "patrimonio_netto", "debiti_totali", "debiti_finanziari",
                "totale_attivo", "attivo_corrente", "passivo_corrente",
                "interessi_passivi", "oneri_finanziari", "immobilizzazioni",
                "immobilizzazioni_prec", "ricavi_anno_prec"
            ]
        }

        logger.debug(f'Dati di bilancio puliti: {bilancio_pulito}')
    indici = calcola_indici(bilancio_pulito)
    logger.debug(f'Indici calcolati: {indici}')
        macro_area = assegna_macro_area(indici)
    logger.debug(f'Macro area assegnata: {macro_area}')

        # Estrazione bandi filtrati
        bandi = estrai_bandi(macro_area, dimensione)
    logger.debug(f'Bandi estratti: {bandi[:3]}')

        # Invio a Claude per selezione finale
        azienda_data = {
            "regione": input_data.anagrafica.get("regione", ""),
            "codice_ateco": input_data.anagrafica.get("codice_ateco", ""),
            "dimensione": dimensione,
            "indici": indici
        }

        logger.debug(f'Dati per Claude: {azienda_data}')
    commento = classifica_bandi_claude(bandi, azienda_data)
    logger.debug(f'Commento Claude: {commento}')

        return {
            "macro_area": macro_area,
            "dimensione": dimensione,
            "z_score": indici.get("Z_Score", "N/D"),
            "mcc_rating": indici.get("MCC", "N/D"),
            "bandi_raccomandati": commento
        }

    except Exception as e:
        return {"errore": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
