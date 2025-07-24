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
url = f"https://api.short.io/links/{SHORT_LINK_ID}/statistics"
headers = {
    "accept": "application/json",
    "authorization": SHORTIO_API_KEY
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    clicks = data.get("clicks", 0)

    supabase.table("shortio_stats").insert({
        "link_id": SHORT_LINK_ID,
        "ref_code": None,
        "date": str(today),  # puoi anche usare yesterday
        "clicks": clicks
    }).execute()

    print(f"✅ Click salvati per il {today}: {clicks}")
else:
    print(f"❌ Errore API Short.io: {response.status_code} – {response.text}")
