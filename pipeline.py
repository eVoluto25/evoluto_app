
import logging
from email_sender import invia_email
from bandi_matcher import calcola_match_bando
from prefiltraggio_bandi import filtra_bandi_per_macroarea
from output_generator import genera_motivazione_bando, calcola_impatto_simulato, simula_beneficio, simula_impatto_totale, genera_snippet_analisi
from utils import carica_dati_azienda, salva_top5_bandi

def pipeline(dati_azienda, azienda_id, email_destinatario):
    logging.info("🚀 Avvio pipeline per azienda: %s", azienda_id)

    # Step 1: Pre-filtraggio dei bandi per macroarea
    logging.info("🎯 Step 1: Pre-filtraggio per macroarea")
    macroarea = dati_azienda.get("macroarea")
    bandi_filtrati = filtra_bandi_per_macroarea(macroarea)

    # Step 2: Calcolo punteggi per ogni bando
    logging.info("📊 Step 2: Calcolo punteggi bandi")
    risultati_match = []
    for bando in bandi_filtrati:
        punteggio = calcola_match_bando(bando, dati_azienda)
        bando["punteggio"] = punteggio
        risultati_match.append(bando)

    # Step 3: Selezione Top 5 bandi
    top5_bandi = sorted(risultati_match, key=lambda x: x["punteggio"], reverse=True)[:5]
    salva_top5_bandi(azienda_id, top5_bandi)

    # Step 4: Motivazione, impatto e beneficio
    logging.info("🧠 Step 3: Analisi approfondita bandi selezionati")
    top5_bandi_finali = []
    for bando in top5_bandi:
        motivazione = genera_motivazione_bando(bando, dati_azienda)
        impatto = calcola_impatto_simulato(bando, dati_azienda)
        beneficio = simula_beneficio(bando, dati_azienda)
        bando["motivazione"] = motivazione
        bando["impatto_stimato"] = impatto
        bando["beneficio"] = beneficio
        top5_bandi_finali.append(bando)

    # Step 5: Snippet GPT finale
    logging.info("📩 Step 4: Generazione snippet per GPT")
    snippet_gpt = genera_snippet_analisi(dati_azienda, top5_bandi_finali)
    simulazione = simula_impatto_totale(dati_azienda, top5_bandi_finali)
    snippet_gpt += f"\n\n{simulazione}"

    # Step 6: Invio email
    logging.info("📤 Step 5: Invio risultato via email")
    oggetto = "🔎 Opportunità strategiche per la tua azienda"
    invia_email(email_destinatario, oggetto, snippet_gpt)
    logging.info("✅ Pipeline completata con successo per %s", azienda_id)
