import requests
import json
import pandas as pd

# Intestazioni di autenticazione
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyYm55b2Rsa3JlaGVtbGF6dGFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMjE3ODgsImV4cCI6MjA2Mjg5Nzc4OH0.e1haV4Y8yma9L36bcjy0V7rB6dg3SDPzfwKSyX22Bfk",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyYm55b2Rsa3JlaGVtbGF6dGFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDczMjE3ODgsImV4cCI6MjA2Mjg5Nzc4OH0.e1haV4Y8yma9L36bcjy0V7rB6dg3SDPzfwKSyX22Bfk"
}

# Endpoint
url = "https://arbnyodlkrehemlaztal.supabase.co/rest/v1/bandi_disponibili"

# Richiesta GET
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

# Converti JSON
data = response.json()

# DataFrame
df = pd.DataFrame(data)

# Verifica che la colonna esista
if "data_chiusura_clean" not in df.columns:
    raise ValueError("La colonna 'data_chiusura_clean' non è presente nei dati.")

# Conversione date
df["data_chiusura_clean"] = pd.to_datetime(df["data_chiusura_clean"], errors="coerce")

# Filtro bandi attivi
df_filtrato = df[
    df["data_chiusura_clean"].isna() | (df["data_chiusura_clean"] >= pd.Timestamp.today())
]

# Salva JSON
# Converte tutte le colonne di tipo datetime in stringa ISO
for col in df_filtrato.select_dtypes(include=["datetime64[ns]"]).columns:
    df_filtrato[col] = df_filtrato[col].dt.strftime("%Y-%m-%d")
    
with open("opendata-export.json", "w", encoding="utf-8") as f:
    json.dump(df_filtrato.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

print(f"File aggiornato con {len(df_filtrato)} bandi attivi.")
