import requests
import json
import pandas as pd

# Intestazioni di autenticazione con la tua anon key corretta
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyYm55b2Rsa3JlaGVtbGF6dGFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMjE3ODgsImV4cCI6MjA2Mjg5Nzc4OH0.e1haV4Y8yma9L36bcjy0V7rB6dg3SDPzfwKSyX22Bfk",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyYm55b2Rsa3JlaGVtbGF6dGFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMjE3ODgsImV4cCI6MjA2Mjg5Nzc4OH0.e1haV4Y8yma9L36bcjy0V7rB6dg3SDPzfwKSyX22Bfk"
}

# Endpoint della tabella principale
url = "https://arbnyodlkrehemlaztal.supabase.co/rest/v1/bandi_disponibili"

# Richiesta GET
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

# Converti in JSON
data = response.json()

# Converte in DataFrame
df = pd.DataFrame(data)

# Verifica che la colonna Data_chiusura esista
if "Data_chiusura" not in df.columns:
    raise ValueError("La colonna 'Data_chiusura' non è presente nei dati.")

# Converte Data_chiusura in datetime
df["Data_chiusura"] = pd.to_datetime(df["Data_chiusura"], errors="coerce")

# Filtra i bandi con data di chiusura >= oggi
df_filtrato = df[df["Data_chiusura"] >= pd.Timestamp.today()]

# Converte di nuovo in lista di dict
dati_filtrati = df_filtrato.to_dict(orient="records")

# Salva il file JSON con indentazione leggibile
with open("opendata-export.json", "w", encoding="utf-8") as f:
    json.dump(dati_filtrati, f, ensure_ascii=False, indent=2)

print(f"File 'opendata-export.json' aggiornato con successo. Bandi attivi trovati: {len(dati_filtrati)}")
