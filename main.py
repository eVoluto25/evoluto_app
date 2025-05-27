
import streamlit as st
from plotly_graphs import render_financial_gauges

# Layout principale
st.set_page_config(page_title="eVoluto - Dossier Aziendale", layout="wide")

# Sidebar navigazione
st.sidebar.markdown("## Navigazione")
if st.sidebar.button("Cruscotto"):
    st.switch_page("main.py")
if st.sidebar.button("Elenco Bandi"):
    st.switch_page("pagine/1_elenco_bandi.py")
if st.sidebar.button("Relazioni AI"):
    st.switch_page("pagine/2_relazioni_ai.py")
if st.sidebar.button("Carica Documenti"):
    st.switch_page("pagine/3_carica_documenti.py")

# Titolo e benvenuto
st.title("📊 Dossier di Verifica Aziendale")
st.markdown("Benvenuto nel cruscotto. Carica i documenti per iniziare l’analisi.")

# Esempio di grafici indicatori (inizialmente con valori zero)
st.subheader("📈 Indicatori Finanziari Chiave")
example_indicators = {
    "Capacità di autofinanziamento": 0,
    "Disponibilità liquide": 0,
    "Indebitamento": 0,
    "Utile netto": 0,
    "EBITDA": 0
}
render_financial_gauges(example_indicators)
