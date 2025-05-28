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

response = requests.get(JSON_URL)
data = response.json()

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
