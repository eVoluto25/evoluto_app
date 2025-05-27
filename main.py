
import streamlit as st
import base64
from PIL import Image
import os

# Impostazioni pagina
st.set_page_config(page_title="Dossier di Verifica Aziendale", layout="wide")

# Colori personalizzati con sfondo scuro
st.markdown("""
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
        color: white;
    }
    .css-1aumxhk {
        background-color: black;
        color: white;
    }
    .stButton>button {
        background-color: white;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dossier di Verifica Aziendale")

# Opzione di caricamento file
caricamento = st.radio("🗂️ Scegli come vuoi caricare i documenti",
                       ["📄 File unico (Visura + Bilancio formato XBRL)", "🔴 Due file separati"])

# Condizionale per mostrare il caricamento corretto
if caricamento == "📄 File unico (Visura + Bilancio formato XBRL)":
    st.subheader("Carica il Documento Unico (PDF)")
    file_unico = st.file_uploader("Carica file", type=["pdf"])
else:
    st.subheader("Carica la Visura Camerale (PDF)")
    file_visura = st.file_uploader("Carica Visura", type=["pdf"])
    st.subheader("Carica il Bilancio (PDF)")
    file_bilancio = st.file_uploader("Carica Bilancio", type=["pdf"])

# Spazio prima dell'analisi
st.markdown("## Risorse ancora disponibili per la Tua Azienda")

# Placeholder per box infografici
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Totale Fondi Attivi", value="€0", delta=None)
with col2:
    st.metric(label="Fondi Compatibili", value="€0", delta=None)
with col3:
    st.metric(label="Probabilità Media di Successo", value="ND", delta=None)

# Avviso pre-analisi
st.info("⚠️ Carica i documenti per visualizzare l’analisi e i grafici relativi ai bandi disponibili.")

# Barra di caricamento + immagine
with st.spinner("Analisi in corso..."):
    if os.path.exists("immagini/loading.png"):
        image = Image.open("immagini/loading.png")
        st.image(image, use_column_width=True)

# Placeholder bandi
st.subheader("Top 10 Bandi Disponibili")
st.write("⚠️ I grafici e le informazioni verranno mostrati dopo il caricamento dei documenti.")
