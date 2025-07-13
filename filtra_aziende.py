# -*- coding: utf-8 -*-
import pandas as pd
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
# CARICAMENTO DATI DA FILE UNICO
# -------------------------
df = pd.read_csv("aziende_unificate.csv")

# Normalizzazione
df["forma_giuridica"] = df["forma_giuridica"].apply(normalizza_forma_giuridica)
df["fatturato"] = df["fatturato"].apply(pulisci_fatturato)

# -------------------------
# FILTRI
# -------------------------
filtrate = df[
    df["forma_giuridica"].apply(is_societa_capitale) &
    df["fatturato"] >= FATTURATO_MINIMO
].copy()

# -------------------------
# METADATI E EXPORT
# -------------------------
filtrate["data_filtraggio"] = datetime.now().strftime("%Y-%m-%d")
filtrate["completezza_dati"] = filtrate.notnull().sum(axis=1)

campi_finali = [
    "ragione_sociale", "codice_ateco", "settore", "fatturato", "numero_dipendenti",
    "forma_giuridica", "partita_iva", "sede_legale", "regione", "provincia", "comune",
    "telefono", "cellulare", "email", "sito_web", "data_filtraggio", "completezza_dati"
]

filtrate[campi_finali].to_csv("aziende_filtrate.csv", index=False, encoding="utf-8-sig")
print("✅ CSV generato: aziende_filtrate.csv")
