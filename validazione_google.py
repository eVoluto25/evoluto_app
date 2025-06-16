
import os
import requests

def cerca_google_bando(titolo_bando, regione=None):
    API_KEY = os.getenv("GOOGLE_API_KEY")
    CX = os.getenv("GOOGLE_CX_ID")

    if not API_KEY or not CX:
        raise ValueError("API Key o CX ID mancanti nelle variabili ambiente.")

    query = f"{titolo_bando} fondi disponibili"
    if regione:
        query += f" {regione}"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": 5
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {
            "validato": False,
            "fondi_disponibili": False,
            "messaggio": "⚠️ Errore nella richiesta a Google API.",
            "results": []
        }

    risultati = response.json().get("items", [])

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

    return {
        "validato": validato,
        "fondi_disponibili": fondi,
        "messaggio": messaggio,
        "results": risultati
    }
