import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_analysis_email(azienda):
    subject = f"Analisi completata per {azienda}"
    body = f"""
    Ciao,

    La verifica aziendale per la società "{azienda}" è stata completata con successo.
    Il foglio Google Sheets è stato aggiornato con i dati finanziari e la lista dei bandi selezionati.

    ✅ Puoi ora visualizzare i risultati.

    Saluti,
    il Team eVoluto
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        EMAIL_SENDER = str(EMAIL_SENDER).replace('\xa0', ' ').encode('utf-8').decode('utf-8')
        EMAIL_PASSWORD = str(EMAIL_PASSWORD).replace('\xa0', ' ').encode('utf-8').decode('utf-8')
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

def invia_notifica_email():
    subject = "📢 Aggiornamento completato: Tabella bandi"
    body = f"""
    
    Ciao,

    La tabella dei bandi è stata aggiornata con i dati più recenti.

    ✅ Puoi consultare subito la tabella su Supabase.

    Saluti,
    il Team eVoluto
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
