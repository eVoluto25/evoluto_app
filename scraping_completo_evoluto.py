# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from datetime import datetime
from urllib.parse import quote_plus

# -------------------------
# CONFIG GENERALE
# -------------------------
REGIONI_TARGET = ["Lazio", "Puglia", "Sicilia", "Campania", "Calabria"]
AZIENDE_TOTALE_MAX = 200
DELAY_RANGE = (2, 4)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}

# -------------------------
# SCRAPER 1 – Infoimprese.it
# -------------------------
def scrape_infoimprese():
    risultati = []
    per_regione = AZIENDE_TOTALE_MAX // 5
    for regione in REGIONI_TARGET:
        url = f"https://www.infoimprese.it/Imprese?regione={quote_plus(regione)}&pagina=1"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            boxes = soup.select("div.risultatoRicerca")
            for box in boxes[:per_regione]:
                nome = box.find("h2")
                info = box.find("p")
                sito = box.find("a", href=True)
                risultati.append({
                    "ragione_sociale": nome.text.strip() if nome else None,
                    "sede_legale": info.text.strip() if info else None,
                    "sito_web": sito["href"] if sito else None,
                    "fonte": "infoimprese.it",
                    "regione": regione
                })
            time.sleep(random.uniform(*DELAY_RANGE))
        except:
            continue
    return risultati

# -------------------------
# SCRAPER 2 – PagineGialle.it
# -------------------------
def scrape_paginegialle():
    risultati = []
    per_regione = AZIENDE_TOTALE_MAX // 5
    for regione in REGIONI_TARGET:
        url = f"https://www.paginegialle.it/ricerca/aziende+{quote_plus(regione)}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            schede = soup.select(".scheda")
            for box in schede[:per_regione]:
                nome = box.select_one(".denominazione")
                indirizzo = box.select_one(".indirizzo")
                telefono = box.select_one(".telefono")
                sito = box.select_one("a.sito")
                email = box.select_one("a[href^=mailto:"]")
                risultati.append({
                    "ragione_sociale": nome.text.strip() if nome else None,
                    "sede_legale": indirizzo.text.strip() if indirizzo else None,
                    "telefono": telefono.text.strip() if telefono else None,
                    "email": email['href'].replace("mailto:", "") if email else None,
                    "sito_web": sito['href'] if sito else None,
                    "fonte": "paginegialle.it",
                    "regione": regione
                })
            time.sleep(random.uniform(*DELAY_RANGE))
        except:
            continue
    return risultati

# -------------------------
# SCRAPER 3 – ReportAziende.it (HTML semplice)
# -------------------------
def scrape_reportaziende():
    risultati = []
    base_url = "https://www.reportaziende.it"
    for regione in REGIONI_TARGET:
        url = f"{base_url}/ricerca?regione={quote_plus(regione)}&tipo=SRL"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            righe = soup.select(".azienda")
            for riga in righe[:AZIENDE_TOTALE_MAX // 5]:
                nome = riga.select_one("h2")
                link = riga.select_one("a")
                href = base_url + link['href'] if link else None
                risultati.append({
                    "ragione_sociale": nome.text.strip() if nome else None,
                    "sito_web": href,
                    "fonte": "reportaziende.it",
                    "regione": regione
                })
            time.sleep(random.uniform(*DELAY_RANGE))
        except:
            continue
    return risultati

# -------------------------
# SCRAPER 4 – OpenCorporates (via API)
# -------------------------
def scrape_opencorporates():
    risultati = []
    base_url = "https://api.opencorporates.com/v0.4/companies/search?q=italy&jurisdiction_code=it"
    try:
        r = requests.get(base_url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            js = r.json()
            for entry in js.get("results", {}).get("companies", [])[:AZIENDE_TOTALE_MAX // 5]:
                dati = entry["company"]
                risultati.append({
                    "ragione_sociale": dati.get("name"),
                    "partita_iva": dati.get("company_number"),
                    "forma_giuridica": dati.get("company_type"),
                    "sede_legale": dati.get("registered_address"),
                    "fonte": "opencorporates",
                    "regione": "-"
                })
    except:
        pass
    return risultati

# -------------------------
# SCRAPER 5 – Completamento da sito aziendale
# -------------------------
def completa_con_scraping_sito(azienda):
    if not azienda.get("sito_web"):
        return azienda
    try:
        r = requests.get(azienda["sito_web"], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        testo = soup.get_text().lower()
        if not azienda.get("email"):
            match = pd.Series(re.findall(r"[\w\.-]+@[\w\.-]+", testo))
            if not match.empty:
                azienda["email"] = match.iloc[0]
        if not azienda.get("cellulare"):
            match = pd.Series(re.findall(r"\+39\s?3\d{2}[\s.-]?\d{6,7}", testo))
            if not match.empty:
                azienda["cellulare"] = match.iloc[0]
    except:
        pass
    return azienda

# -------------------------
# UNIONE + EXPORT
# -------------------------
print("⏳ Avvio scraping completo...")
info1 = scrape_infoimprese()
info2 = scrape_paginegialle()
info3 = scrape_reportaziende()
info4 = scrape_opencorporates()

# Unione e completamento
dataset = info1 + info2 + info3 + info4
finale = []
for az in dataset:
    finale.append(completa_con_scraping_sito(az))

# Esporta CSV finale
df = pd.DataFrame(finale)
df["data_scraping"] = datetime.now().strftime("%Y-%m-%d")
df.to_csv("aziende_unificate.csv", index=False, encoding="utf-8-sig")
print(f"✅ Scraping completato: {len(df)} aziende salvate in aziende_unificate.csv")
