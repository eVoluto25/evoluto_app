# -*- coding: utf-8 -*-
import pandas as pd
import re
from datetime import datetime

# -------------------------
# CONFIGURAZIONE FILTRI
# -------------------------
FORMA_GIURIDICA_CAPITALE = ["S.r.l.", "S.p.A.", "S.a.p.a."]
FATTURATO_MINIMO = 1_000_000

# -------------------------
# FUNZIONI DI SUPPORTO
# -------------------------
def pulisci_fatturato(val):
    if pd.isnull(val):
        return None
    val = str(val).replace("€", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(val)
    except:
        return None

def normalizza_forma_giuridica(val):
    if not isinstance(val, str):
        return ""
    val = val.strip().upper()
    if "SRL" in val:
        return "S.r.l."
    if "SPA" in val:
        return "S.p.A."
    if "SAPA" in val:
        return "S.a.p.a."
    return val.title()

def is_societa_capitale(val):
    return val in FORMA_GIURIDICA_CAPITALE

# -------------------------
# CARICAMENTO DATI MULTIFONTE (mock example)
# -------------------------
# Simulazione di merge tra più fonti
infoimprese = pd.read_csv("infoimprese.csv")
kompass = pd.read_csv("kompass.csv")
paginegialle = pd.read_csv("paginegialle.csv")

# Merge base su ragione sociale
merged = infoimprese.merge(kompass, on="ragione_sociale", how="outer")
merged = merged.merge(paginegialle, on="ragione_sociale", how="outer")

# Pulizia e normalizzazione
merged["forma_giuridica"] = merged["forma_giuridica"].apply(normalizza_forma_giuridica)
merged["fatturato"] = merged["fatturato"].apply(pulisci_fatturato)

# -------------------------
# FILTRI APPLICATI
# -------------------------
filtrate = merged[
    merged["forma_giuridica"].apply(is_societa_capitale) &
    merged["fatturato"] >= FATTURATO_MINIMO
].copy()

# -------------------------
# AGGIUNTA METADATI E EXPORT
# -------------------------
filtrate["data_scraping"] = datetime.now().strftime("%Y-%m-%d")
filtrate["completezza_dati"] = filtrate.notnull().sum(axis=1)

# Selezione colonne finali per export
campi_finali = [
    "ragione_sociale", "codice_ateco", "settore", "fatturato", "numero_dipendenti",
    "forma_giuridica", "partita_iva", "sede_legale", "regione", "provincia", "comune",
    "telefono", "cellulare", "email", "sito_web", "data_scraping", "completezza_dati"
]

filtrate[campi_finali].to_csv("aziende_filtrate.csv", index=False, encoding="utf-8-sig")
print("CSV generato: aziende_filtrate.csv")
