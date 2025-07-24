import os
import requests
from datetime import datetime
from supabase import create_client, Client

# --- Variabili ambiente ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SHORTIO_API_KEY = os.getenv("SHORTIO_API_KEY")
SHORT_LINK_ID = os.getenv("SHORT_LINK_ID")

# --- Supabase client ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Oggi (UTC) ---
today = datetime.utcnow().date()

# --- Short.io API - GET totale click ---
url = f"https://api.short.io/links/{SHORT_LINK_ID}"
headers = {
    "accept": "application/json",
    "authorization": SHORTIO_API_KEY
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    total_clicks = data.get("clicks", 0)

    # --- Recupera ultimo record salvato ---
    previous = (
        supabase.table("shortio_stats")
        .select("date", "clicks")
        .order("date", desc=True)
        .limit(1)
        .execute()
    )

    if previous.data:
        last_clicks = previous.data[0]["clicks"]
        clicks_giornalieri = total_clicks - last_clicks
    else:
        clicks_giornalieri = total_clicks  # primo inserimento

    # --- Scrivi su Supabase ---
    result = supabase.table("shortio_stats").insert({
        "link_id": SHORT_LINK_ID,
        "ref_code": None,
        "date": str(today),
        "clicks": total_clicks,
        "clicks_giornalieri": clicks_giornalieri
    }).execute()

    print(f"✅ Click salvati per il {today}: totali={total_clicks}, giornalieri={clicks_giornalieri}")
else:
    print(f"❌ Errore API Short.io: {response.status_code} – {response.text}")
