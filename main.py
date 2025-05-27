
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from plotly_graphs import render_financial_gauges
from PIL import Image

# Titolo
st.set_page_config(page_title="Dossier di Verifica Aziendale", layout="wide")

st.title("📊 Dossier di Verifica Aziendale")

# Sezione Fondi
st.markdown("### 💰 Risorse ancora disponibili per la Tua Azienda")
col1, col2, col3 = st.columns(3)
col1.metric("Totale Fondi Attivi", "€0")
col2.metric("Fondi Compatibili", "€0")
col3.metric("Probabilità Media di Successo", "ND")

# Sezione Dimensioni Economiche
st.markdown("### 📌 Dimensioni Economiche")
col4, col5 = st.columns(2)
col4.metric("Fatturato Annuo", "€0")
col5.metric("Totale Attivo di Bilancio", "€0")

# Indicatori Finanziari
st.markdown("### 📉 Indicatori Finanziari Chiave")
render_financial_gauges({
    "Capacità di autofinanziamento": 0,
    "Disponibilità liquide": 0,
    "Indebitamento": 0,
    "Utile netto": 0,
    "EBITDA": 0,
})

# Caricamento documento
st.markdown("### 📎 Carica il Documento Unico (PDF)")
st.write("Carica il documento PDF contenente la Visura Camerale e il Bilancio.")
st.file_uploader("Carica file", type=["pdf"], label_visibility="collapsed")
