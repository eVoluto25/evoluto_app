import requests
from bs4 import BeautifulSoup
import logging

# Configura logger
logger = logging.getLogger("estrazione_bandi")
logger.setLevel(logging.INFO)

# Stampa anche su console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def estrai_estratto_bando(titolo_bando):
    url_base = "https://www.incentivi.gov.it/incentivi?search="
    url = f"{url_base}{titolo_bando.replace(' ', '%20')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        estratto = ""
        blocchi_testo = soup.find_all("p")
        for p in blocchi_testo:
            testo = p.get_text(strip=True)
            if 80 <= len(testo) <= 300:
                estratto = testo
                break

        if not estratto:
            estratto = "ℹ️ Nessun estratto disponibile o struttura non riconosciuta."

        logger.info(f"[OK] Estratto ottenuto per: '{titolo_bando}'")

        return {
            "link": url,
            "estratto": estratto
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"[ERRORE] Titolo: '{titolo_bando}' → {e}")
        return {
            "link": url,
            "estratto": f"❌ Errore durante l’accesso al bando '{titolo_bando}'. Controlla su incentivi.gov manualmente."
        }
