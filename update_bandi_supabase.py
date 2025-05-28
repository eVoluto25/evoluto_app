import requests
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://<tuo-progetto>.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<tua-service-role-key>")
TABLE_NAME = "bandi_disponibili"
JSON_URL = "https://www.incentivi.gov.it/sites/default/files/open-data/2025-4-5_opendata-export.json"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(JSON_URL, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
    except Exception as e:
        print("Errore durante il parsing del JSON:", e)
        exit(1)
else:
    print(f"Errore nel recupero dei dati: {response.status_code}")
    exit(1)

oggi = datetime.today().date()
bandi_aperti = []
for bando in data:
    chiusura = bando.get("Data_chiusura")
    if not chiusura or datetime.strptime(chiusura, "%Y-%m-%d").date() > oggi:
        bandi_aperti.append(bando)

print(f"Bandi aperti trovati: {len(bandi_aperti)}")

for record in bandi_aperti:
    supabase.table(TABLE_NAME).upsert(record, on_conflict=["ID_Incentivo"]).execute()

print("Aggiornamento completato.")
