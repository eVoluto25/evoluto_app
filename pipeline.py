import json
import logging
import smtplib
from email.mime.text import MIMEText
from bandi_matcher import trova_bandi_compatibili
from scoring_engine_ready import macroarea_match
from output_gpt import genera_output_gpt, genera_commento_bandi
from gpt_formatter import genera_snippet_analisi
from impatto_simulato import calcola_impatto_simulato, simula_beneficio, simula_impatto_totale
from motivazione_bando import genera_motivazione_bando

logging.basicConfig(level=logging.INFO)

def invia_email(destinatario, oggetto, contenuto):
    mittente = "info@capitaleaziendale.it"  
    msg = MIMEText(contenuto)
    msg['Subject'] = oggetto
    msg['From'] = mittente
    msg['To'] = destinatario

    try:
        with smtplib.SMTP('localhost') as server:
            server.sendmail(mittente, [destinatario], msg.as_string())
        print(f"📩 Email inviata a {destinatario}")
    except Exception as e:
        logging.error(f"Errore invio email: {e}")

def esegui_pipeline_intermedio(analisi_json):
    try:
        dati_azienda = json.loads(analisi_json)
        azienda_id = dati_azienda.get("partita_iva", "00000000000")
        logging.info(f"📥 Avvio pipeline per azienda {azienda_id}")

        # Step 4: Ricerca bandi
        logging.info("🎯 Step 4: Ricerca bandi compatibili")
        trova_bandi_compatibili(azienda_id, dati_azienda)
        print("✅ Bandi compatibili salvati")

        # Step 5: Calcolo punteggi
        logging.info("📈 Step 5: Calcolo punteggi bandi")
        calcola_punteggi_bandi(azienda_id)
        print("✅ Punteggi calcolati")

        # Step 6: Generazione output GPT
        logging.info("💬 Step 6: Generazione output GPT")
        output = genera_output_gpt(azienda_id)
        print("✅ Output GPT generato")

        top5_bandi = dati_azienda.get("top5_bandi", [])
        top5_bandi_finali = []

        for bando in top5_bandi:
            motivazione = genera_motivazione_bando(bando, dati_azienda)
            impatto = calcola_impatto_simulato(bando, dati_azienda)
            beneficio = simula_beneficio(bando, dati_azienda)
            bando["motivazione"] = motivazione
            bando["impatto_stimato"] = impatto
            bando["beneficio"] = beneficio
            top5_bandi_finali.append(bando)

        snippet = genera_snippet_analisi(dati_azienda, {}, dati_azienda.get("macroarea"), top5_bandi_finali)
        commenti = genera_commento_bandi(top5_bandi_finali)
        snippet += "\n\n🧠 Opportunità selezionate:\n" + commenti

        simulazione = simula_impatto_totale(dati_azienda, top5_bandi_finali)
        snippet += f"\n\n{simulazione}"

        print(snippet)

        # Invio email
        destinatario = dati_azienda.get("email", "info@capitaleaziendale.it")
        invia_email(destinatario, "📊 Report Verifica Aziendale", snippet)

    except Exception as e:
        logging.error(f"Errore in pipeline: {e}")
