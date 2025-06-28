import requests
import json

# Intestazioni per autenticazione
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyYm55b2Rsa3JlaGVtbGF6dGFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMjE3ODgsImV4cCI6MjA2Mjg5Nzc4OH0.e1haV4Y8yma9L36bcjy0V7rB6dg3SDPzfwKSyX22Bfk",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyYm55b2Rsa3JlaGVtbGF6dGFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMjE3ODgsImV4cCI6MjA2Mjg5Nzc4OH0.e1haV4Y8yma9L36bcjy0V7rB6dg3SDPzfwKSyX22Bfk"
}

# Endpoint della view
url = "https://arbnyodlkrehmelaztal.supabase.co/rest/v1/bandi_disponibili"

# Richiesta GET
response = requests.get(url, headers=headers)
data = response.json()

# Salva il file con il nome richiesto
with open("opendata-export.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("File opendata-export.json aggiornato con successo.")
