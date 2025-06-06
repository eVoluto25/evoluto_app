import os
from simulatore_impatto import simula_beneficio
from gpt_formatter import genera_snippet_analisi
from impatto_simulato import calcola_impatto_simulato
from pdf_cleaner import pulisci_pdf
from bilancio import calcola_indici_finanziari
from macroarea import assegna_macroarea
from bandi_matcher import trova_bandi_compatibili
from valutazione_punteggio import calcola_valutazione
from output_gpt import genera_output_gpt 

def estrai_testo_da_base64(base64_pdf: str) -> str:
    """
    Decodifica un PDF base64, lo salva temporaneamente e ne estrae il testo.
    """
    try:
        path_temp = "/tmp/temp_input.pdf"
        pdf_bytes = base64.b64decode(base64_pdf)

        with open(path_temp, "wb") as f:
            f.write(pdf_bytes)

        testo = ""
        with fitz.open(path_temp) as doc:
            for pagina in doc:
                testo += pagina.get_text()

        return testo.strip()
    except Exception as e:
        return f"❌ Errore estrazione testo PDF: {str(e)}"

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
    dati_analisi = supabase.table("verifica_aziendale").select("*").eq("id", azienda_id).execute().data[0]
    genera_output_html_e_scrivi(azienda_id, dati_analisi)
    print("✅ HTML salvato nella colonna verifica_html")

    return output

    processa_analisi_pdf = esegui_pipeline
