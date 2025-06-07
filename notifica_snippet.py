
from supabase import create_client, Client
import requests
import json
import smtplib
from email.message import EmailMessage
from datetime import datetime

# --- CONFIGURAZIONE ---

SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_SERVICE_ROLE_KEY"
SUPABASE_BANDI_TABLE = "bandi"
SUPABASE_ANALISI_TABLE = "verifica_aziendale"

EMAIL_SENDER = "tuoindirizzo@email.com"
EMAIL_PASSWORD = "TUA_PASSWORD_APP"
EMAIL_RECIPIENT = "tuo_cliente@email.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- CONNESSIONE SUPABASE ---

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNZIONE: INVIA EMAIL ---

def invia_email(oggetto, corpo):
    msg = EmailMessage()
    msg["Subject"] = oggetto
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT
    msg.set_content(corpo)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

# --- FUNZIONE: NOTIFICA AGGIORNAMENTO BANDI ---

def notifica_aggiornamento_bandi():
    oggi = datetime.utcnow().date()
    bandi = supabase.table(SUPABASE_BANDI_TABLE).select("*").gte("data_aggiornamento", str(oggi)).execute().data

    if bandi:
        corpo = "🟢 Sono stati trovati nuovi bandi aggiornati oggi:\n\n"
        for bando in bandi:
            corpo += f"- {bando['titolo']} ({bando['territorio']})\n"
        invia_email("Nuovi bandi disponibili oggi", corpo)

# --- FUNZIONE: INVIA SNIPPET COMPLETO ANALISI ---

def invia_snippet_analisi(id_azienda):
    dati = supabase.table(SUPABASE_ANALISI_TABLE).select("*").eq("id", id_azienda).execute().data
    if not dati:
        print("⚠️ Nessun dato trovato per questa azienda.")
        return

    analisi = dati[0]
    corpo = "📊 RISULTATI ANALISI DI BILANCIO\n\n"
    corpo += f"Ragione sociale: {analisi.get('ragione_sociale', 'N/D')}\n"
    corpo += f"Anno: {analisi.get('anno', 'N/D')}\n"
    corpo += f"Macro Area: {analisi.get('macroarea', 'N/D')}\n\n"

    corpo += "🔍 INDICI:\n"
    for k, v in analisi.items():
        if k.startswith("indice_"):
            corpo += f"- {k.replace('indice_', '').replace('_', ' ').title()}: {v}\n"

    corpo += "\n📌 OPPORTUNITÀ:\n"
    bandi = analisi.get("bandi_suggeriti", [])
    if not bandi:
        corpo += "Nessun bando disponibile\n"
    else:
        for bando in bandi:
            corpo += f"- {bando}\n"

    invia_email(f"Snippet analisi bilancio - {analisi.get('ragione_sociale', 'Azienda')}", corpo)

# --- ESECUZIONE COMBINATA ---

if __name__ == "__main__":
    notifica_aggiornamento_bandi()
    invia_snippet_analisi(id_azienda="ID_AZIENDA_DA_INSERIRE")
