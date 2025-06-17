import os
import requests
import logging

logger = logging.getLogger(__name__)

def cerca_google_bando(titolo_bando, regione=None):
    API_KEY = os.getenv("GOOGLE_API_KEY")
    CX = os.getenv("GOOGLE_CX_ID")

    logger.info(f"▶️ Avvio validazione con Google: '{titolo_bando}' | Regione: '{regione}'")

    if not API_KEY or not CX:
        raise ValueError("API Key o CX ID mancanti nelle variabili ambiente.")

    query = f"{titolo_bando} bando attivo"
    if regione:
        query += f" {regione}"

    logger.info(f"🔎 Query generata per Google API: {query}")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": 5
    }

    response = requests.get(url, params=params)
    
    logger.info(f"📩 Risposta ricevuta da Google API | Status: {response.status_code}")

    if response.status_code != 200:
        return {
            "validato": False,
            "fondi_disponibili": False,
            "messaggio": "⚠️ Errore nella richiesta a Google API.",
            "results": []
        }

    logger.error("❌ Errore nella risposta di Google API.")

    risultati = response.json().get("items", [])

    if not risultati:
        logger.warning("🟨 Nessun risultato restituito da Google API.")
    else:
        for i, item in enumerate(risultati):
            logger.info(f"🔹 Risultato {i+1}: {item.get('title')} | Snippet: {item.get('snippet')}")

    # Analizza i primi 5 snippet
    validato = any("aperto" in item.get("snippet", "").lower() or "proroga" in item.get("snippet", "").lower() for item in risultati)
    fondi = any("fondi" in item.get("snippet", "").lower() or "disponibile" in item.get("snippet", "").lower() for item in risultati)

    messaggio = ""
    if validato:
        messaggio += "✅ Validato online."
    else:
        messaggio += "⚠️ Non validato da fonti ufficiali."

    if fondi:
        messaggio += " 💰 Fondi ancora disponibili secondo fonti pubbliche."
    else:
        messaggio += " ❌ Fondi risultano esauriti o non verificabili."

    logger.info(f"📊 Esito validazione Google → Validato: {validato} | Fondi: {fondi}")

    return {
        "validato": validato,
        "fondi_disponibili": fondi,
        "messaggio": messaggio,
        "results": risultati
    }
