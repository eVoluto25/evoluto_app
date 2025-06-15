import json
import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from query_supabase import get_bandi_filtrati

app = FastAPI()

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Abilitazione CORS per permettere chiamate da altri domini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analizza-azienda")
async def analizza_azienda(request: Request):
    try:
        data = await request.json()
        logger.info("Dati ricevuti da GPT: %s", json.dumps(data, indent=2))

        macro_area = data.get("macro_area")
        codice_ateco = data.get("codice_ateco")
        regione = data.get("regione")
        dimensione = data.get("dimensione")

        # Verifica campi obbligatori
        if not all([macro_area, codice_ateco, regione, dimensione]):
            return {"errore": "Dati mancanti per l'interrogazione. Verifica macro_area, codice_ateco, regione, dimensione."}

        # Interrogazione tabella corretta in Supabase
        bandi_filtrati = get_bandi_filtrati(macro_area, codice_ateco, regione, dimensione, max_results=25)

        # Estrazione variabili chiave da passare a Claude
        z_score = data.get("z_score", "ND")
        mcc_rating = data.get("mcc_rating", "ND")
        utile_netto = data.get("utile_netto", 0)

        logger.info("Bandi filtrati trovati: %d", len(bandi_filtrati))

        return {
            "bandi": bandi_filtrati,
            "z_score": z_score,
            "mcc_rating": mcc_rating,
            "utile_netto": utile_netto,
            "dimensione": dimensione
        }

    except Exception as e:
        logger.error("Errore nell'analisi aziendale: %s", str(e))
        return {"errore": f"Errore durante l'elaborazione: {str(e)}"}
