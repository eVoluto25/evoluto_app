
import streamlit as st
from PIL import Image
from gpt_module import run_gpt_analysis
from claude_module import match_with_bandi
from supabase_utils import fetch_bandi

st.set_page_config(page_title="eVoluto - Dossier di Verifica Aziendale", layout="wide")

st.title("📊 Dossier di Verifica Aziendale")

# Sezione 1 - Fondi disponibili
st.markdown("## 💰 Risorse ancora disponibili per la Tua Azienda")
col1, col2, col3 = st.columns(3)
col1_val = "€0"
col2_val = "€0"
col3_val = "ND"
col1.metric("Totale Fondi Attivi", col1_val)
col2.metric("Fondi Compatibili", col2_val)
col3.metric("Probabilità Media di Successo", col3_val)

# Sezione 2 - Fatturato e Totale Attivo
st.markdown("### 📌 Dimensioni Economiche")
c1, c2 = st.columns(2)
fatturato = "€0"
attivo = "€0"
c1.metric("Fatturato Annuo", fatturato)
c2.metric("Totale Attivo di Bilancio", attivo)

# Sezione 3 - Indicatori Finanziari
st.markdown("### 📉 Indicatori Finanziari Chiave")
from plotly_graphs import render_financial_gauges
render_financial_gauges()

# Sezione 4 - Caricamento documento
st.markdown("### 📂 Caricamento Documenti Aziendali")
uploaded_file = st.file_uploader("Carica il Documento Unico (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Analisi in corso..."):
        img = Image.open("immagini/loading.png")
        st.image(img, use_column_width=True)

        # Estrazione + GPT
        with open("temp_input.pdf", "wb") as f:
            f.write(uploaded_file.read())

        indici = run_gpt_analysis("temp_input.pdf")
        bandi = fetch_bandi()
        bandi_compatibili, bandi_extra, fondi_totali, fondi_compatibili, probabilita = match_with_bandi(indici, bandi)

        # Aggiorna dashboard
        col1.metric("Totale Fondi Attivi", f"€{fondi_totali:,}")
        col2.metric("Fondi Compatibili", f"€{fondi_compatibili:,}")
        col3.metric("Probabilità Media di Successo", f"{probabilita}%")
        c1.metric("Fatturato Annuo", f"€{indici.get('fatturato', 0):,}")
        c2.metric("Totale Attivo di Bilancio", f"€{indici.get('attivo', 0):,}")
        render_financial_gauges(indici)

        # Mostra bandi compatibili
        st.markdown("## 🧾 Bandi Compatibili con l’Azienda")
        for i, bando in enumerate(bandi_compatibili):
            st.markdown(f"**{i+1}. {bando['titolo']}**")
            st.markdown(f"✔️ Compatibilità: {bando['compatibilità']}")
            st.markdown(f"📌 Motivazione: {'; '.join(bando['motivazione'])}")
            if bando['criticità']:
                st.error(f"⚠️ Criticità: {'; '.join(bando['criticità'])}")

        with st.expander("🔎 Mostra altri 10 bandi compatibili"):
            for bando in bandi_extra:
                st.markdown(f"**{bando['titolo']}**")
                st.markdown(f"✔️ Compatibilità: {bando['compatibilità']}")
                st.markdown(f"📌 Motivazione: {'; '.join(bando['motivazione'])}")
                if bando['criticità']:
                    st.warning(f"⚠️ Criticità: {'; '.join(bando['criticità'])}")
