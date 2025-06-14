from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any
from analisi_finanziaria import calcola_indici, assegna_macro_area, calcola_dimensione
from query_supabase import estrai_bandi
from scoring_claude import classifica_bandi_claude

app = FastAPI()

class AziendaInput(BaseModel):
    anagrafica: Dict[str, Any]
    bilancio: Dict[str, float]

@app.post("/analizza-azienda")
def analizza_azienda(input_data: AziendaInput):
    # Calcolo dimensione e indici
    dimensione = calcola_dimensione(
        input_data.anagrafica["dipendenti"],
        input_data.bilancio["ricavi"],
        input_data.bilancio["totale_attivo"]
    )

    indici = calcola_indici(input_data.bilancio)
    macro_area = assegna_macro_area(indici)

    # Estrazione bandi filtrati
    bandi = estrai_bandi(
        macro_area=macro_area,
        codice_ateco=input_data.anagrafica["codice_ateco"],
        regione=input_data.anagrafica["regione"],
        dimensione=dimensione
    )

    # Invio a Claude per selezione finale
    azienda_data = {
        "regione": input_data.anagrafica["regione"],
        "codice_ateco": input_data.anagrafica["codice_ateco"],
        "dimensione": dimensione,
        "macro_area": macro_area,
        "indici": indici
    }

    commento = classifica_bandi_claude(bandi, azienda_data)

    return {
       "macro_area": macro_area,
        "dimensione": dimensione,
        "z_score": indici.get("Z_Score"),
        "mcc_rating": indici.get("MCC", "N/D"),
        "bandi_raccomandati": commento
    }
