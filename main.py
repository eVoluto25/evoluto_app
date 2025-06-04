from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from estrazione import estrai_indici, assegna_macroarea
from utils import supabase_query_esteso, supabase_insert
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/match_bandi")
async def match_bandi(req: Request):
    data = await req.json()
    logger.info(f"Richiesta ricevuta: {data}")

    try:
        azienda = data.get("azienda", "ND")
        anagrafica = {k: data.get(k, "") for k in [
            "forma_giuridica", "codice_ateco", "partita_iva", "anno_fondazione",
            "numero_dipendenti", "attivita_prevalente", "provincia", "citta", "amministratore"
        ]}

        indici = estrai_indici(data)
        macroarea = assegna_macroarea(indici)

        filtro_bandi = {
            "macroarea": macroarea,
            "Tipologia_Soggetto": anagrafica["forma_giuridica"],
            "Dimensioni": anagrafica["numero_dipendenti"],
            "Settore_Attivita": anagrafica["attivita_prevalente"],
            "Codici_ATECO": anagrafica["codice_ateco"],
            "Regioni": anagrafica.get("provincia", ""),
            "Comuni": anagrafica.get("citta", "")
        }

        bandi = supabase_query_esteso("bandi_disponibili", filtro_bandi)
        id_bandi = [bando.get("ID_Incentivo") for bando in bandi if "ID_Incentivo" in bando]

        verifica_data = {
            "azienda": azienda,
            "macroarea": macroarea,
            "ID_Incentivo": id_bandi,
            **indici,
            **anagrafica
        }

        logger.info(f"Salvataggio su verifica_aziendale: {verifica_data}")
        supabase_insert("verifica_aziendale", verifica_data)

        return {
            "azienda": azienda,
            "macroarea": macroarea,
            "bandi_compatibili": bandi
        }
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione: {e}")
        return {"errore": str(e)}
