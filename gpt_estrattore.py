# gpt_estrattore.py

import requests
import os
import logging
import json

GPT_API_URL = os.getenv("RENDER_GPT_URL", "https://render-gpt.example.com/estrai")
GPT_API_KEY = os.getenv("RENDER_GPT_API_KEY")

VARIABILI_ATTESE = {
    "anagrafica": [
        "codice_fiscale", "regione", "dimensione_impresa"
    ],
    "bilancio": [
        "ricavi", "ebitda", "utile_netto", "patrimonio_netto",
        "totale_attivo", "totale_passivo", "totale_debiti",
        "oneri_finanziari", "liquidita", "crediti", "debiti_brevi",
        "immobilizzazioni", "passivo_consolidato", "attivo_corrente",
        "passivo_corrente", "cassa", "pfn", "interessi_attivi",
        "cash_flow_operativo", "rimanenze", "totale_fonti"
    ]
}

def inferisci_dimensione_impresa(bilancio: dict) -> str:
    ricavi = bilancio.get("ricavi", 0)
    addetti = bilancio.get("addetti", 0)

    if ricavi < 2_000_000:
        return "micro"
    elif ricavi < 10_000_000:
        return "piccola"
    elif ricavi < 50_000_000 or addetti < 250:
        return "media"
    return "grande"

def estrai_dati_pdf(file_path: str) -> dict:
    headers = {
        "Authorization": f"Bearer {GPT_API_KEY}"
    }

    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/pdf")}
            response = requests.post(GPT_API_URL, headers=headers, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()

        if "anagrafica" not in result:
            result["anagrafica"] = {}

        if "bilancio" not in result:
            result["bilancio"] = {}

        # Parsing anagrafica da visura: normalizzazione base
        raw = result.get("anagrafica", {})
        cf = raw.get("codice_fiscale") or raw.get("cf") or raw.get("piva")
        regione = raw.get("regione") or raw.get("provincia") or raw.get("sede_legale")

        result["anagrafica"]["codice_fiscale"] = cf
        result["anagrafica"]["regione"] = regione

        # Inferenza automatica dimensione da bilancio
        dimensione = inferisci_dimensione_impresa(result["bilancio"])
        result["anagrafica"]["dimensione_impresa"] = dimensione

        # Controllo campi mancanti
        mancano = {}
        for sezione, chiavi in VARIABILI_ATTESE.items():
            presenti = result.get(sezione, {})
            assenti = [k for k in chiavi if k not in presenti]
            if assenti:
                mancano[sezione] = assenti
        if mancano:
            logging.warning(f"Campi mancanti GPT: {mancano}")
            result["warning"] = {"campi mancanti": mancano}

        return result

    except Exception as e:
        logging.error(f"Errore estrazione GPT: {e}")
        return {"errore": str(e)}