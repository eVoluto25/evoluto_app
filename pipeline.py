import json
import logging
from email_sender import invia_email_output
from bandi_matcher import trova_bandi_compatibili
from scoring import calcola_punteggi_bandi
from output_gpt import genera_output_gpt, genera_snippet_analisi, genera_commento_bandi
from simulazioni import genera_motivazione_bando, calcola_impatto_simulato, simula_beneficio, simula_impatto_totale

def pipeline_analisi(azienda_id, dati_azienda, indici, macroarea):
    logging.info("🚀 Avvio pipeline analisi per azienda: %s", azienda_id)

    # Step 4: Ricerca bandi compatibili
    logging.info("🎯 Step 4: Ricerca bandi compatibili")
    trova_bandi_compatibili(azienda_id, dati_azienda)
    print("✅ Bandi compatibili salvati")

    # Step 5: Calcolo punteggi bandi
    logging.info("📈 Step 5: Calcolo punteggi bandi")
    calcola_punteggi_bandi(azienda_id)
    print("✅ Punteggi calcolati")

    # Step 6: Generazione output GPT
    logging.info("💬 Step 6: Generazione output GPT")
    output = genera_output_gpt(azienda_id)
    print("✅ Output GPT generato")

    top5 = dati_azienda.get("top5_bandi", [])
    commenti = genera_commento_bandi(top5)
    output += "\n\n🧠 Opportunità selezionate:\n" + commenti

    # Step 7: Dettagli per top 5 bandi
    top5_bandi_finali = []
    for bando in top5:
        motivazione = genera_motivazione_bando(bando, dati_azienda)
        impatto = calcola_impatto_simulato(bando, dati_azienda)
        beneficio = simula_beneficio(bando, dati_azienda)
        bando["motivazione"] = motivazione
        bando["impatto_stimato"] = impatto
        top5_bandi_finali.append(bando)

    # Step 8: Generazione snippet finale per GPT
    snippet_gpt = genera_snippet_analisi(dati_azienda, indici, macroarea, top5_bandi_finali)
    print(snippet_gpt)

    # Step 9: Simulazione impatto complessivo
    simulazione = simula_impatto_totale(dati_azienda, top5_bandi_finali)
    snippet_gpt += f"\n\n{simulazione}"

    # Step 10: Invio risultato via email
    email_cliente = dati_azienda.get("email", "destinatario@esempio.com")
    oggetto = f"📊 Risultato Analisi – {dati_azienda.get('ragione_sociale', '')}"
    invia_email_output(email_cliente, oggetto, snippet_gpt)
    print("✅ Email inviata al cliente.")