import streamlit as st
from extractor import extract_data_from_pdf
from gpt_module import run_gpt_analysis
from claude_module import match_with_bandi
from supabase_utils import fetch_bandi

# Tema personalizzato
st.markdown("""
    <style>
        .stApp {
            background-color: #000000;
            color: white;
        }
        .stButton>button {
            background-color: white;
            color: black;
        }
        .css-1cpxqw2, .css-1d391kg {
            background-color: #f0f2f6;
        }
    </style>
""", unsafe_allow_html=True)

# Titolo e opzioni
st.title("Dossier di Verifica Aziendale")
st.markdown("#### 📂 Scegli come vuoi caricare i documenti")

caricamento = st.radio(
    "",
    ("📄 File unico (Visura + Bilancio formato XBRL)", "🔴 Due file separati")
)

file_visura = None
file_bilancio = None
file_unico = None

if caricamento == "📄 File unico (Visura + Bilancio formato XBRL)":
    file_unico = st.file_uploader("Carica il Documento Unico (PDF)", type="pdf", key="unico")
else:
    file_visura = st.file_uploader("Carica la Visura Camerale (PDF)", type="pdf", key="visura")
    file_bilancio = st.file_uploader("Carica il Bilancio (PDF)", type="pdf", key="bilancio")

st.markdown("## Risorse ancora disponibili per la Tua Azienda")
st.markdown("### Top 10 Bandi Disponibili")

if not file_visura and not file_bilancio and not file_unico:
    st.info("⚠️ Carica i documenti per visualizzare l’analisi e i grafici relativi ai bandi disponibili.")
else:
    with st.spinner("🔍 Analisi in corso..."):
        # Estrazione dati
        if file_unico:
            visura_data, bilancio_data = extract_data_from_pdf(file_unico, unico=True)
        else:
            visura_data = extract_data_from_pdf(file_visura) if file_visura else {}
            bilancio_data = extract_data_from_pdf(file_bilancio) if file_bilancio else {}

        dati_completi = {**visura_data, **bilancio_data}

        # Analisi GPT + Claude + Recupero bandi
        analisi = run_gpt_analysis(dati_completi)
        bandi = fetch_bandi()
        risultati = match_with_bandi(dati_completi, bandi)

        # Output
        for idx, risultato in enumerate(risultati[:10], 1):
            st.markdown(f"### {idx}. {risultato['titolo']}")
            st.markdown(f"**Compatibilità:** {risultato['grado']}")
            st.markdown(f"**Motivazione:** {risultato['motivazione']}")
            if risultato['criticità']:
                st.warning(f"⚠️ Criticità: {risultato['criticità']}")
