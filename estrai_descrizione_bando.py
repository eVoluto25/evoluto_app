import os
import re
import json
import logging
import requests
from bs4 import BeautifulSoup

# Configura log
logging.basicConfig(
    filename="estrazione_bandi.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://www.incentivi.gov.it"
SEARCH_URL = f"{BASE_URL}/incentivi?search="
CACHE_FILE = "cache_bandi.json"

# Carica cache se esiste
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}

def salva_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def limita_estratto_intelligente(testo: str, max_parole=200) -> str:
    parole = testo.split()
    if len(parole) <= max_parole:
        return testo.strip()

    testo_tagliato = " ".join(parole[:max_parole])
    frasi = re.split(r'(?<=[.!?]) +', testo_tagliato)
    if frasi:
        testo_finale = " ".join(frasi[:-1]) if len(frasi) > 1 else frasi[0]
        return testo_finale.strip() + "..."
    else:
        return testo_tagliato.strip() + "..."

def estrai_estratto_bando(titolo_bando_esatto: str) -> dict:
    """
    Cerca il bando su incentivi.gov.it e restituisce il link e il paragrafo introduttivo (estratto).
    """
    if titolo_bando_esatto in cache:
        logging.info(f"Cache hit per: {titolo_bando_esatto}")
        return cache[titolo_bando_esatto]

    try:
        logging.info(f"Ricerca bando: {titolo_bando_esatto}")
        response = requests.get(SEARCH_URL + titolo_bando_esatto, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        risultati = soup.select("a.card-incentivo")
        for link in risultati:
            titolo = link.get_text(strip=True)
            if titolo_bando_esatto.lower() in titolo.lower():
                url_bando = BASE_URL + link.get("href")
                dettaglio = requests.get(url_bando, timeout=10)
                dettaglio.raise_for_status()
                soup_bando = BeautifulSoup(dettaglio.text, "html.parser")

                intro = soup_bando.select_one("div.testo-incentivo p")
                descrizione = intro.get_text(strip=True) if intro else "Descrizione non disponibile"
                descrizione_finale = limita_estratto_intelligente(descrizione)

                risultato = {
                    "link": url_bando,
                    "estratto": descrizione_finale
                }
                cache[titolo_bando_esatto] = risultato
                salva_cache()
                logging.info(f"Bando trovato: {titolo}")
                return risultato

        risultato = {
            "link": None,
            "estratto": "Bando non trovato."
        }
        cache[titolo_bando_esatto] = risultato
        salva_cache()
        logging.warning(f"Nessun bando trovato per: {titolo_bando_esatto}")
        return risultato

    except Exception as e:
        logging.error(f"Errore per {titolo_bando_esatto}: {str(e)}")
        return {
            "link": None,
            "estratto": f"Errore durante lo scraping: {str(e)}"
        }
