import requests
import json
import pandas as pd

# Intestazioni di autenticazione
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyYm55b2Rsa3JlaGVtbGF6dGFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMjE3ODgsImV4cCI6MjA2Mjg5Nzc4OH0.e1haV4Y8yma9L36bcjy0V7rB6dg3SDPzfwKSyX22Bfk",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyYm55b2Rsa3JlaGVtbGF6dGFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMjE3ODgsImV4cCI6MjA2Mjg5Nzc4OH0.e1haV4Y8yma9L36bcjy0V7rB6dg3SDPzfwKSyX22Bfk"
}

# Endpoint tabella principale
url = "https://arbnyodlkrehmelaztal.supabase.co/rest/v1/bandi_disponibili"

# Richiesta GET
response = requests.get(url, headers=headers)
data = response.json()

# Filtra bandi attivi
df = pd.DataFrame(data)
df["Data_chiusura"] = pd.to_datetime(df["Data_chiusura"], errors="coerce")
df = df[df["Data_chiusura"] >= pd.Timestamp.today()]

# Salva JSON
with open("opendata-export.json", "w", encoding="utf-8") as f:
    json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

print("File opendata-export.json aggiornato solo con bandi attivi.")
