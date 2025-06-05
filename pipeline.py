
import os
from pdf_cleaner import extract_and_clean_text
from bilancio import calcola_indici_e_scrivi
from macroarea import assegna_macroarea
from bandi_matcher import trova_bandi_compatibili
from valutazione_punteggio import calcola_punteggi_bandi
from gpt_output import genera_output_gpt

def esegui_pipeline(nome_file, percorso_file):
    print(f"🔍 Inizio analisi per: {nome_file}")

    # Step 1: Estrazione e pulizia del file (XBRL, PDF, DOCX)
    testo_pulito = extract_and_clean_text(percorso_file)
    print("✅ Estrazione e pulizia completata")

    # Step 2: Calcolo indici finanziari e scrittura su Supabase
    azienda_id = calcola_indici_e_scrivi(nome_file, testo_pulito)
    print(f"✅ Calcolo indici completato per azienda ID: {azienda_id}")

    # Step 3: Assegnazione macro area
    assegna_macroarea(azienda_id)
    print("✅ Macroarea assegnata")

    # Step 4: Ricerca bandi compatibili
    trova_bandi_compatibili(azienda_id)
    print("✅ Bandi compatibili salvati")

    # Step 5: Calcolo punteggi bandi
    calcola_punteggi_bandi(azienda_id)
    print("✅ Punteggi calcolati")

    # Step 6: Generazione output GPT
    output = genera_output_gpt(azienda_id)
    print("✅ Output GPT generato")

    return output
