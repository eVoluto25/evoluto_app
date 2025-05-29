
import streamlit as st
from auth import login_user
from extractor import process_uploaded_files
from streamlit_dashboard import render_dashboard
from export_streamlit_data import export_results
from config import DASHBOARD_TITLE

# Titolo dell'applicazione
st.set_page_config(page_title=DASHBOARD_TITLE, layout="wide")

# Login e autenticazione
user_authenticated, username = login_user()

if user_authenticated:
    st.success(f"Benvenuto, {username}!")

    # Area di caricamento file
    st.sidebar.header("📁 Caricamento Documenti")
    uploaded_balance = st.sidebar.file_uploader("Carica il bilancio in formato XBRL", type=["xbrl"])
    uploaded_visura = st.sidebar.file_uploader("Carica la visura camerale (PDF)", type=["pdf"])

    start_analysis = st.sidebar.button("📊 Avvia Analisi")

    # Mostra il cruscotto anche se non sono stati caricati documenti
    analysis_data = None
    company_info = None

    if start_analysis and (uploaded_balance or uploaded_visura):
        with st.spinner("⏳ Elaborazione documenti in corso..."):
            company_info, analysis_data = process_uploaded_files(uploaded_balance, uploaded_visura)

    # Cruscotto
    render_dashboard(company_info, analysis_data)

    # Esportazione risultati
    export_results()
else:
    st.warning("🔒 Effettua il login per accedere al cruscotto.")
