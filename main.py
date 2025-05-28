
import streamlit as st
import pandas as pd
from parse_xbrl import estrai_dati_bilancio, estrai_anagrafica_visura
from classificazione_macro_area import assegna_macroarea
from export_streamlit_data import visualizza_anagrafica, visualizza_analisi_finanziaria, visualizza_risultati_bandi
from scoring_bandi import calcola_scoring_bandi
from logs import log_evento

# Titolo dashboard
st.title("Analisi Finanziaria & Matching Bandi - eVoluto")

# Caricamento documenti
st.sidebar.header("Carica i documenti")
uploaded_xbrl = st.sidebar.file_uploader("Bilancio XBRL (.xml)", type=["xml"])
uploaded_visura = st.sidebar.file_uploader("Visura Camerale (.pdf)", type=["pdf"])

if st.sidebar.button("Avvia Analisi"):

    if not uploaded_xbrl or not uploaded_visura:
        st.error("Carica sia il bilancio XBRL che la visura camerale per procedere.")
    else:
        # Log: caricamento file
        log_evento("File caricati: avvio analisi")

        # Estrazione dati
        dati_bilancio = estrai_dati_bilancio(uploaded_xbrl)
        anagrafica = estrai_anagrafica_visura(uploaded_visura)

        # Visualizzazione anagrafica
        st.subheader("📌 Dati Anagrafici Azienda")
        visualizza_anagrafica(anagrafica)

        # Analisi finanziaria
        st.subheader("📊 Analisi Finanziaria")
        visualizza_analisi_finanziaria(dati_bilancio)

        # Macroarea
        macroarea = assegna_macroarea(dati_bilancio)
        st.success(f"📌 Macroarea Finanziaria Assegnata: {macroarea}")

        # Invio GPT + Claude (automatizzato)
        log_evento("Analisi inviata a GPT e Claude")

        # Simulazione ricezione bandi (verranno da Claude prefiltrati + scoring)
        df_bandi = pd.read_csv("data/bandi_filtrati.csv")
        bandi_con_punteggio = calcola_scoring_bandi(df_bandi, dati_bilancio)

        # Visualizzazione e filtro
        st.subheader("🎯 Bandi Suggeriti")
        visualizza_risultati_bandi(bandi_con_punteggio)

        # Export
        csv = bandi_con_punteggio.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Esporta in CSV", data=csv, file_name="bandi_suggeriti.csv", mime="text/csv")
