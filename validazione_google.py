import os
import requests
import logging

# Imposta il logging (utile se non già impostato altrove)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cerca_google_bando(titolo_bando):
    API_KEY = os.getenv("GOOGLE_API_KEY")
    CX = os.getenv("GOOGLE_CX_ID")

    if not API_KEY or not CX:
        logger.error("❌ API Key o CX ID mancanti nelle variabili ambiente.")
        raise ValueError("API Key o CX ID mancanti nelle variabili ambiente.")

    query = f"{titolo_bando} bando"
    logger.info(f"🔍 Query generata per Google API: {query}")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": 5
    }

    try:
        response = requests.get(url, params=params)
        logger.info(f"📡 Risposta ricevuta da Google API | Status: {response.status_code}")
    except Exception as e:
        logger.exception("❌ Errore durante la richiesta a Google API.")
        return {
            "validato": False,
            "estratto": "",
            "esito": "❌ Errore nella connessione a Google API."
        }

    if response.status_code != 200:
        return {
            "validato": False,
            "estratto": "",
            "esito": "⚠️ Errore nella richiesta a Google API."
        }

    risultati = response.json().get("items", [])

    if not risultati:
        logger.warning("⚠️ Nessun risultato restituito da Google API.")
        return {
            "validato": False,
            "estratto": "",
            "esito": "❌ Nessun risultato trovato online."
        }

    for i, item in enumerate(risultati):
        logger.info(f"🔎 Risultato {i+1}: {item.get('title')} | Link: {item.get('link')}")

        titolo_google = item.get("title", "").lower()
        if titolo_bando.lower() in titolo_google:
            snippet = item.get("snippet", "")
            estratto = ' '.join(snippet.split()[:30])
            titolo_pagina = item.get("title", "")[:100]
            logger.info("✅ Validazione completata con esito positivo.")
            return {
                "validato": True,
                "estratto": estratto,
                "esito": f"✅ Verificato online\n📄 Titolo: {titolo_pagina}\n📌 Estratto: {estratto}..."
            }

    logger.info("❌ Nessuna corrispondenza trovata nei risultati.")
    return {
        "validato": False,
        "estratto": "",
        "esito": "❌ Nessun risultato compatibile trovato online."
    }
