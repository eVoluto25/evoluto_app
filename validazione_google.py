import os
import requests
import logging

def cerca_google_bando(titolo_bando, regione=None):

    logger = logging.getLogger(__name__)

    API_KEY = os.getenv("GOOGLE_API_KEY")
    CX = os.getenv("GOOGLE_CX_ID")

    if not API_KEY or not CX:
        raise ValueError("API Key o CX ID mancanti nelle variabili ambiente.")

    query = f"{titolo_bando} bando attivo"
    logger.info(f"🔍 Query generata per Google API: {query}")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": 5
    }

    response = requests.get(url, params=params)
    logger.info(f"📡 Risposta ricevuta da Google API | Status: {response.status_code}")

    if response.status_code != 200:
        return {
            "validato": False,
            "fondi_disponibili": False,
            "messaggio": "⚠️ Errore nella richiesta a Google API.",
            "results": []
        }

    logger.error("❌ Errore nella risposta di Google API.")
    risultati = response.json().get("items", [])
    messaggio = ""
    validato = False

    if not risultati:
        logger.warning("⚠️ Nessun risultato restituito da Google API.")
    else:
        for i, item in enumerate(risultati):
            logger.info(f"🔎 Risultato {i+1}: {item.get('title')} | Snippet: {item.get('snippet')}")
        
        # 🎯 Confronto flessibile sul titolo
        titolo_normalizzato = titolo_bando.lower()
        for item in risultati:
            titolo_google = item.get("title", "").lower()
            if any(parola in titolo_google for parola in titolo_normalizzato.split() if len(parola) > 3):
                validato = True
                titolo_pagina = item.get('title', '')[:100]
                raw_snippet = item.get('snippet', '').strip().replace('\n', ' ')
                estratto_snippet = ' '.join(raw_snippet.split()[:30])
                messaggio = f"✅ Verificato online\n📄 Titolo: {titolo_pagina}\n📌 Estratto: {estratto_snippet}..."
                break

    # 💬 Restituzione risultato finale
    return {
        "validato": validato,
        "fondi_disponibili": False,
        "messaggio": messaggio if validato else "❌ Nessun risultato compatibile trovato online.",
        "results": risultati[:3]
    }

    for item in risultati:
        titolo_google = item.get("title", "").lower()
    
        # confronta se almeno una parola significativa è contenuta
        match = any(parola in titolo_google for parola in titolo_normalizzato.split())

        if match:
            logger.info(f"✅ Titolo compatibile trovato: {titolo_google}")
            validato = True
            break
    
    # 💰 Verifica presenza fondi
    fondi = any(
        any(kw in item.get("snippet", "").lower() for kw in keywords_fondi)
        for item in risultati
    )

    # 🔁 Nuova logica: se il titolo del bando è presente, validiamo comunque
    if not validato:
        titolo_match = any(
            titolo_bando.lower() in item.get("title", "").lower() or
            titolo_bando.lower() in item.get("snippet", "").lower()
            for item in risultati
        )
        if titolo_match:
            validato = True
            titolo_pagina = item.get("title", "")
            raw_snippet = item.get("snippet", "").replace('\n', ' ').strip()
            estratto_snippet = ' '.join(raw_snippet.split()[:25])
    
            logger.info(f"✅ Titolo trovato: {titolo_pagina}")
            messaggio += f"✅ Validato online\n📄 Titolo: {titolo_pagina}\n📌 Estratto: {estratto_snippet}..."

    messaggio = ""
    if validato:
        messaggio += "✅ Validato online."
    else:
        messaggio += "⚠️ Non validato da fonti ufficiali."

    logger.info(f"📊 Esito validazione Google → Validato: {validato}")

    return {
        "validato": validato,
        "fondi_disponibili": fondi,
        "messaggio": messaggio,
        "results": risultati[:5]
    }
