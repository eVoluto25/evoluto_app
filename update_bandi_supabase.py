import requests
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://<tuo-progetto>.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<tua-service-role-key>")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "bandi_disponibili"
import json  # aggiungi se non c'è

JSON_PATH = "./data/2025-4-5_opendata-export.json"

try:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
        data = raw.get("response", {}).get("docs", [])
        if not isinstance(data, list):
            print("❌ Errore: il JSON non è una lista di bandi.")
            exit(1)
except Exception as e:
    print("Errore durante la lettura del file locale JSON:", e)
    exit(1)

oggi = datetime.today().date()
bandi_aperti = []
for bando in data:
    if isinstance(bando, dict):  # ✅ Verifica che sia un dizionario
        chiusura = bando.get("Data_chiusura")
        if not chiusura or datetime.strptime(chiusura, "%Y-%m-%dT%H:%M:%S").date() > oggi:
            bandi_aperti.append(bando)
    else:
        print("Elemento non valido (non è un dizionario):", bando)

print(f"Bandi aperti trovati: {len(bandi_aperti)}")

for record in bandi_aperti:
    supabase.table(TABLE_NAME).upsert(record, on_conflict=["ID_Incentivo"]).execute()

print("Aggiornamento completato.")
