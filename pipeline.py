import os
from gpt_formatter import genera_snippet_analisi
from pdf_cleaner import pulisci_pdf
from bilancio import calcola_indici_finanziari
from macroarea import assegna_macroarea
from bandi_matcher import trova_bandi_compatibili
from valutazione_punteggio import calcola_valutazione
from output_gpt import genera_output_gpt 

def esegui_pipeline(nome_file, percorso_file):
    print(f"🔍 Inizio analisi per: {nome_file}")

    # Step 1: Estrazione e pulizia del file (XBRL, PDF, DOCX)
    testo_pulito = extract_and_clean_text(percorso_file)
    print("✅ Estrazione e pulizia completata")

    # Step 2: Calcolo indici finanziari e scrittura su Supabase
    azienda_id = calcola_indici_e_scrivi(nome_file, testo_pulito)
    print(f"✅ Calcolo indici completato per azienda ID: {azienda_id}")

    # Recupero dati finanziari per logiche avanzate
    dati_azienda = supabase.table("verifica_aziendale").select("utile_netto,liquidita,fatturato").eq("id", azienda_id).execute().data[0]

    # Step 3: Assegnazione macro area
    assegna_macroarea(azienda_id)
    print("✅ Macroarea assegnata")

    # Step 4: Ricerca bandi compatibili
    trova_bandi_compatibili(azienda_id, dati_azienda)
    print("✅ Bandi compatibili salvati")

    # Step 5: Calcolo punteggi bandi
    calcola_punteggi_bandi(azienda_id)
    print("✅ Punteggi calcolati")

    # Step 6: Generazione output GPT
    output = genera_output_gpt(azienda_id)
    print("✅ Output GPT generato")
    top5 = dati_azienda.get("top5_bandi", [])
    commenti = genera_commento_bandi(top5)
    output += "\n\n🧠 Opportunità selezionate:\n" + commenti

    # Step 7: Salvataggio HTML finale nella colonna verifica_html
    dati_analisi = supabase.table("verifica_aziendale").select("*").eq("id", azienda_id).execute().data[0]
    genera_output_html_e_scrivi(azienda_id, dati_analisi)
    print("✅ HTML salvato nella colonna verifica_html")

    return output
