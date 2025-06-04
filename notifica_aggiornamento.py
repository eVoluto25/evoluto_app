import os
import smtplib
from email.mime.text import MIMEText

def invia_notifica_email():
    mittente = os.getenv("EMAIL_SENDER")
    destinatario = os.getenv("EMAIL_SENDER") 
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText("La tabella bandi_disponibili è stata aggiornata.")
    msg["Subject"] = "📡 Supabase aggiornata"
    msg["From"] = mittente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(mittente, password)
        server.send_message(msg)
