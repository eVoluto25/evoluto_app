import os
import logging
import json
from simulatore_impatto import simula_beneficio
from gpt_formatter import genera_snippet_analisi
from impatto_simulato import calcola_impatto_simulato
from pdf_cleaner import estrai_testo_pymupdf
from bilancio import estrai_dati_bilancio_completo
from macroarea import assegna_macroarea
from bandi_matcher import trova_bandi_compatibili
from valutazione_punteggio import calcola_valutazione
from output_gpt import genera_output_gpt 

def esegui_pipeline_intermediario_json(data: dict) -> str:
    logging.info("🚀 Avvio pipeline da GPT con dati strutturati")

    # Step 1: Validazione dati minimi
    richiesti = [
        "ragione_sociale", "codice_ateco", "forma_giuridica", "partita_iva", 
        "attivita_prevalente", "provincia", "citta", "data_costituzione", 
        "dipendenti", "dimensione", "amministratore", "fatturato", "utile_netto",
        "ebitda", "ebitda_margin", "ricerca_sviluppo", "costi_ambientali", 
        "totale_attivo", "liquidita", "immobilizzazioni", "indebitamento", 
        "debt_equity", "current_ratio", "interest_coverage", "autofinanziamento", 
        "investimenti"
    ]
    for campo in richiesti:
        if campo not in data:
            raise ValueError(f"❌ Campo mancante: {campo}")

    # Step 2: Scrittura su Supabase e assegnazione macroarea
    azienda_id = scrivi_dati_completi_su_supabase(data)  # da creare

    logging.info("📌 ID azienda generato: %s", azienda_id)

    assegna_macroarea(azienda_id)

    # Step 3: Trova bandi e genera output
    bandi = trova_bandi_compatibili(azienda_id)
    output = genera_output_gpt(azienda_id, bandi)

    return output

    # Step 2: Calcolo indici finanziari e scrittura su Supabase
    logging.info("📘 Step 1: Calcolo indici finanziari e salvataggio su Supabase")
    dati_dict = json.loads(testo_pulito)  # converte la stringa in dizionario
    dati_bilancio = estrai_dati_bilancio_completo(dati_dict)
    azienda_id = calcola_indici_finanziari(nome_file, dati_bilancio)

    # Recupero dati finanziari per logiche avanzate
    logging.info("📦 Step 2: Recupero dati aziendali da Supabase")

    # Step 3: Assegnazione macro area
    logging.info("📊 Step 3: Assegnazione macroarea")
    assegna_macroarea(azienda_id)
    print("✅ Macroarea assegnata")

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
    # Dopo il calcolo dei top 5 bandi e dei punteggi (dati_azienda e indici già esistenti)
    motivazione = genera_motivazione_bando(bando, dati_azienda) 
    impatto = calcola_impatto_simulato(bando, dati_azienda)
    bando["motivazione"] = motivazione
    beneficio = simula_beneficio(bando, dati_azienda)
    bando["impatto_stimato"] = impatto
    top5_bandi_finali.append(bando)

    # Aggiunge impatto stimato e motivazione sintetica ai top 5
    top5_bandi_finali = []
    for bando in top5_bandi:
        motivazione = genera_motivazione_bando(bando, dati_azienda)  
        impatto = calcola_impatto_simulato(bando, dati_azienda)
        beneficio = simula_beneficio(bando, dati_azienda)
        bando["motivazione"] = motivazione
        bando["impatto_stimato"] = impatto
        top5_bandi_finali.append(bando)
 
    snippet_gpt = genera_snippet_analisi(dati_azienda, indici, macroarea, top5_bandi)
    print(snippet)  # 🔁 GPT lo legge in chat
    
    # Aggiunta simulazione impatto totale
    simulazione = simula_impatto_totale(dati_azienda, top5_bandi)
    snippet_gpt += f"\n\n{simulazione}"

    # Passa questo snippet alla funzione GPT (ad es. output_gpt)
    output = genera_output_gpt(snippet_gpt)

    # Step 7: Salvataggio HTML finale nella colonna verifica_html
    logging.info("💬 Step 7: Salvataggio output HTML GPT")
    dati_analisi = supabase.table("verifica_aziendale").select("*").eq("id", azienda_id).execute().data[0]
    genera_output_html_e_scrivi(azienda_id, dati_analisi)
    print("✅ HTML salvato nella colonna verifica_html")

    return output

    processa_analisi_pdf = esegui_pipeline
