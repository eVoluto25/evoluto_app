import streamlit as st
import plotly.express as px
import pandas as pd
from extractor import extract_data_from_pdf
from gpt_module import run_gpt_analysis
from claude_module import match_with_bandi
from supabase_utils import fetch_bandi

st.set_page_config(page_title="eVoluto – Dossier di Verifica Aziendale", layout="wide")
st.title("📁 eVoluto – Dossier di Verifica Aziendale")

# Scelta modalità di caricamento
modalità_unico_file = st.radio(
    "📂 Scegli modalità di caricamento",
    ["File unico (Visura + Bilancio)", "Due file separati"],
    horizontal=True
)

azienda_data = None

if modalità_unico_file == "File unico (Visura + Bilancio)":
    uploaded_unico = st.file_uploader("Carica documento PDF unico (Visura + Bilancio)", type="pdf")
    if uploaded_unico and st.button("🔍 Avvia Analisi"):
        azienda_data = extract_data_from_pdf(uploaded_unico, None)
else:
    uploaded_visura = st.file_uploader("Carica Visura Camerale (PDF)", type="pdf")
    uploaded_bilancio = st.file_uploader("Carica Bilancio (PDF)", type="pdf")
    if uploaded_visura and uploaded_bilancio and st.button("🔍 Avvia Analisi"):
        azienda_data = extract_data_from_pdf(uploaded_visura, uploaded_bilancio)

if azienda_data:
    st.header("💰 Opportunità di Finanziamento")
    st.subheader("Top 5 Bandi Disponibili per la Tua Azienda")

    bandi = [
        {"nome": "Bando Innovazione", "importo": 50000},
        {"nome": "Fondo Sviluppo PMI", "importo": 75000},
        {"nome": "Incentivo Ricerca", "importo": 30000},
        {"nome": "Credito Imposta", "importo": 45000},
        {"nome": "Bando Digitalizzazione", "importo": 60000}
    ]

    df_bandi = pd.DataFrame(bandi)
    df_bandi = df_bandi.sort_values(by="importo", ascending=True)

    fig = px.bar(
        df_bandi,
        x="importo",
        y="nome",
        orientation='h',
        labels={'importo': 'Importo (€)', 'nome': 'Bando'},
        text="importo"
    )

    fig.update_traces(texttemplate='%{text:,.0f} €', textposition='outside')
    fig.update_layout(
        title="Top 5 Bandi Disponibili",
        xaxis_title="Importo (€)",
        yaxis_title="",
        yaxis=dict(tickfont=dict(size=12)),
        xaxis=dict(tickfont=dict(size=12)),
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)
