
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Dossier di Verifica Aziendale",
    layout="centered",
    initial_sidebar_state="auto"
)

# Reset tema scuro -> chiaro
st.markdown("""
    <style>
        body {
            background-color: white;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dossier di Verifica Aziendale")
st.markdown("🗂️ <strong>Scegli come vuoi caricare i documenti</strong>", unsafe_allow_html=True)

upload_mode = st.radio(
    "",
    ["📄 File unico (Visura + Bilancio formato XBRL)", "🔴 Due file separati"],
    horizontal=True
)

if upload_mode == "📄 File unico (Visura + Bilancio formato XBRL)":
    st.subheader("Carica il Documento Unico (PDF)")
    uploaded_file = st.file_uploader("Carica file", type=["pdf"])
else:
    st.subheader("Carica la Visura Camerale (PDF)")
    visura_file = st.file_uploader("Carica Visura", type=["pdf"], key="visura")
    st.subheader("Carica il Bilancio (PDF)")
    bilancio_file = st.file_uploader("Carica Bilancio", type=["pdf"], key="bilancio")

# Stato simulato di elaborazione
elaborazione_in_corso = uploaded_file or (upload_mode == "🔴 Due file separati" and visura_file and bilancio_file)

if elaborazione_in_corso:
    with st.spinner("Analisi in corso..."):
        img = Image.open("immagini/loading.png")
        st.image(img, width=300)
        st.markdown("<p style='text-align:center;'>Analisi in corso... ⏳</p>", unsafe_allow_html=True)
        # Qui inserire l'elaborazione vera e propria

# Area risorse
st.subheader("Risorse ancora disponibili per la Tua Azienda")

col1, col2, col3 = st.columns(3)
col1.metric("Totale Fondi Attivi", "€0")
col2.metric("Fondi Compatibili", "€0")
col3.metric("Probabilità Media di Successo", "ND")

st.info("⚠️ I grafici e le informazioni verranno mostrati dopo il caricamento dei documenti.")
