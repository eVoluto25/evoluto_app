
import logging
import json
from email_output import invia_email_output
from scoring_bandi import calcola_punteggi_bandi
from motivazione_bando import genera_motivazione
from impatto_simulato import calcola_impatto_simulato
from output_gpt import genera_snippet_analisi
from simulatore_impatto import simula_beneficio, simula_impatto_totale
from estrazione import carica_bandi_csv

def esegui_pipeline_intermedia(dati_azienda: dict, indici: dict, macroarea: str):
    logging.info("🚀 Avvio analisi Python per selezione bandi compatibili")

    # Step 1: Carica i bandi aperti da Supabase o CSV locale
    logging.info("📥 Step 1: Caricamento bandi aperti")
    bandi_disponibili = carica_bandi_csv()

    # Step 2: Calcolo punteggi per ciascun bando
    logging.info("📊 Step 2: Calcolo punteggi bandi")
    bandi_con_punteggio = calcola_punteggi_bandi(bandi_disponibili, dati_azienda)

    # Ordina per punteggio decrescente
    bandi_ordinati = sorted(bandi_con_punteggio, key=lambda x: x.get("punteggio", 0), reverse=True)
    top5_bandi = bandi_ordinati[:5]

    # Step 3: Aggiunge motivazione, impatto e beneficio per ciascun bando
    logging.info("🧠 Step 3: Motivazione e simulazioni economiche")
    top5_bandi_finali = []
    for bando in top5_bandi:
        bando["motivazione"] = genera_motivazione(bando)
        bando["impatto_stimato"] = calcola_impatto_simulato(bando, dati_azienda)
        bando["beneficio"] = simula_beneficio(bando, dati_azienda)
        top5_bandi_finali.append(bando)

    # Step 4: Simulazione impatto totale
    logging.info("📈 Step 4: Simulazione impatto totale")
    simulazione = simula_impatto_totale(dati_azienda, top5_bandi_finali)

    # Step 5: Generazione snippet GPT
    logging.info("📝 Step 5: Generazione snippet")
    snippet = genera_snippet_analisi(dati_azienda, indici, macroarea, top5_bandi_finali)
    snippet += f"\n\n{simulazione}"

    # Step 6: Invio via email
    logging.info("📧 Step 6: Invio email")
    invia_email_output(snippet)
    logging.info("✅ Analisi completata e inviata.")
