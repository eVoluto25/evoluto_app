import os
import requests
from datetime import datetime, timedelta
from supabase import create_client, Client

# Variabili ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SHORTIO_API_KEY = os.getenv("SHORTIO_API_KEY")
SHORT_LINK_ID = os.getenv("SHORT_LINK_ID")

# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Calcolo date
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

# API Short.io – Statistiche giornaliere
url = f"https://api.short.io/links/{SHORT_LINK_ID}/statistics/by_interval"
headers = {
    "accept": "application/json",
    "authorization": SHORTIO_API_KEY,
    "content-type": "application/json"
}
payload = {
    "from": str(yesterday),
    "to": str(today),
    "interval": "day"
}
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    stats = data.get('statistics', [])
    clicks = stats[0]['clicks'] if stats else 0

    # Controlla se esiste già un record per ieri
    existing = supabase.table("shortio_stats") \
        .select("id") \
        .eq("link_id", SHORT_LINK_ID) \
        .eq("date", str(yesterday)) \
        .execute()

    if existing.data:
        print(f"⚠️ Record già presente per il {yesterday}. Nessun inserimento.")
    else:
        # Inserisce i dati
        supabase.table("shortio_stats").insert({
            "link_id": SHORT_LINK_ID,
            "ref_code": "evoluto",
            "date": str(yesterday),
            "clicks": clicks,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        print(f"✅ Click salvati per il {yesterday}: {clicks}")

else:
    print(f"❌ Errore API Short.io: {response.status_code} – {response.text}")
