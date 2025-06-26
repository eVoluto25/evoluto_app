import os
from fastapi import FastAPI
from supabase import create_client, Client

# Connessione a Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# -------- API: Bandi di Sostegno --------
@app.get("/bandi-sostegno")
def get_bandi_sostegno():
    try:
        response = supabase.table("bandi_sostegno").select(
            "Titolo,Descrizione,Obiettivo_Finalita,Data_apertura,Data_chiusura,"
            "Dimensioni,Tipologia_Soggetto,Forma_agevolazione,Codici_ATECO,Regioni,Ambito_territoriale"
        ).execute()

        print(">>> [DEBUG SOSTEGNO] Risposta Supabase:", response)
        print(">>> [DEBUG SOSTEGNO] Dati:", response.data)

        if not response.data:
            return {
                "data": [],
                "esito": "nessun_bando",
                "messaggio": "Nessun bando disponibile."
            }

        return {
            "data": response.data,
            "esito": "ok"
        }

    except Exception as e:
        print(f">>> [ERRORE API SOSTEGNO]: {e}")
        return {
            "data": [],
            "esito": "errore",
            "messaggio": str(e)
        }

# -------- API: Bandi di Transizione --------
@app.get("/bandi-transizione")
def get_bandi_transizione():
    try:
        response = supabase.table("bandi_transizione").select(
            "Titolo,Descrizione,Obiettivo_Finalita,Data_apertura,Data_chiusura,"
            "Dimensioni,Tipologia_Soggetto,Forma_agevolazione,Codici_ATECO,Regioni,Ambito_territoriale"
        ).execute()

        print(">>> [DEBUG TRANSIZIONE] Risposta Supabase:", response)
        print(">>> [DEBUG TRANSIZIONE] Dati:", response.data)

        if not response.data:
            return {
                "data": [],
                "esito": "nessun_bando",
                "messaggio": "Nessun bando disponibile."
            }

        return {
            "data": response.data,
            "esito": "ok"
        }

    except Exception as e:
        print(f">>> [ERRORE API TRANSIZIONE]: {e}")
        return {
            "data": [],
            "esito": "errore",
            "messaggio": str(e)
        }

# -------- API: Bandi di Digitalizzazione --------
@app.get("/bandi-digitalizzazione")
def get_bandi_digitalizzazione():
    try:
        response = supabase.table("bandi_digitalizzazione").select(
            "Titolo,Descrizione,Obiettivo_Finalita,Data_apertura,Data_chiusura,"
            "Dimensioni,Tipologia_Soggetto,Forma_agevolazione,Codici_ATECO,Regioni,Ambito_territoriale"
        ).execute()

        print(">>> [DEBUG DIGITALIZZAZIONE] Risposta Supabase:", response)
        print(">>> [DEBUG DIGITALIZZAZIONE] Dati:", response.data)

        if not response.data:
            return {
                "data": [],
                "esito": "nessun_bando",
                "messaggio": "Nessun bando disponibile."
            }

        return {
            "data": response.data,
            "esito": "ok"
        }

    except Exception as e:
        print(f">>> [ERRORE API DIGITALIZZAZIONE]: {e}")
        return {
            "data": [],
            "esito": "errore",
            "messaggio": str(e)
        }
