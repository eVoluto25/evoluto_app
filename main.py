
import streamlit as st
import plotly.graph_objects as go
from PIL import Image

# --- Configurazione pagina ---
st.set_page_config(page_title="eVoluto - Dossier di Verifica Aziendale", layout="wide")

# --- Funzione per gauge dinamico ---
def gauge_chart(title, value, min_val, max_val, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': color},
            'bgcolor': "lightgray"
        }
    ))
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), height=200)
    return fig

# --- Layout ---
st.title("📊 Dossier di Verifica Aziendale")
# Spostare 'Risorse disponibili' in alto
st.markdown("""<div style='text-align: center; font-size: 26px; font-weight: bold;'>💰 Risorse ancora disponibili per la Tua Azienda</div>""", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("Totale Fondi Attivi", "€0")
col2.metric("Fondi Compatibili", "€0")
col3.metric("Probabilità Media di Successo", "ND")

# Caricamento documento
st.subheader("Carica il Documento Unico (PDF)")
st.markdown("Carica il documento PDF contenente la Visura Camerale e il Bilancio.")
uploaded_file = st.file_uploader("Carica file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analisi in corso..."):
        # Mostra immagine di caricamento
        img = Image.open("immagini/loading.png")
        st.image(img, use_column_width=True)

# --- Impatto: Sezione Fondi Disponibili ---
st.markdown("## 💰 Risorse ancora disponibili per la Tua Azienda")
cols = st.columns(3)
cols[0].metric("Totale Fondi Attivi", "€0")
cols[1].metric("Fondi Compatibili", "€0")
cols[2].metric("Probabilità Media di Successo", "ND")

# --- Grafici numerici per grandezze aziendali ---
st.markdown("### 📌 Dimensioni Economiche")
col1, col2 = st.columns(2)
col1.metric("Fatturato Annuo", "€0")
col2.metric("Totale Attivo di Bilancio", "€0")

# --- Indicatori Finanziari con Gauge ---
st.markdown("### 📈 Indicatori Finanziari Chiave")
ind1, ind2, ind3 = st.columns(3)
ind4, ind5 = st.columns(2)

with ind1: st.plotly_chart(gauge_chart("Capacità di autofinanziamento", 0, 0, 100, "red"), use_container_width=True)
with ind2: st.plotly_chart(gauge_chart("Disponibilità liquide", 0, 0, 100, "red"), use_container_width=True)
with ind3: st.plotly_chart(gauge_chart("Indebitamento", 0, 0, 100, "red"), use_container_width=True)
with ind4: st.plotly_chart(gauge_chart("Utile netto", 0, 0, 100, "red"), use_container_width=True)
with ind5: st.plotly_chart(gauge_chart("EBITDA", 0, 0, 100, "red"), use_container_width=True)

# --- Placeholder finale ---
st.warning("⚠️ I dati e i grafici verranno aggiornati automaticamente dopo il caricamento dei documenti.")
