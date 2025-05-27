import streamlit as st
from extractor import extract_data_from_pdf
from gpt_module import run_gpt_analysis
from claude_module import match_with_bandi
from supabase_utils import fetch_bandi

st.set_page_config(page_title="eVoluto – Analisi Aziendale", layout="wide")
st.title("📊 eVoluto – Cruscotto Analisi Aziendale")

st.header("📁 Caricamento Documenti Aziendali")
uploaded_visura = st.file_uploader("Carica Visura Camerale (PDF)", type="pdf")
uploaded_bilancio = st.file_uploader("Carica Bilancio (PDF)", type="pdf")

if uploaded_visura and uploaded_bilancio:
    if st.button("🔍 Avvia Analisi"):
        st.info("Estrazione dati aziendali in corso...")
        azienda_data = extract_data_from_pdf(uploaded_visura, uploaded_bilancio)
        st.success("✅ Dati aziendali estratti correttamente")

        st.header("📈 Analisi Finanziaria GPT")
        gpt_result = run_gpt_analysis(azienda_data)

        st.subheader("📊 Dimensione dell’impresa")
        st.metric("Dipendenti", azienda_data["dipendenti"])
        st.metric("Fatturato", f"€ {azienda_data['fatturato']:,}")
        st.metric("Totale Attivo", f"€ {azienda_data['totale_attivo']:,}")

        st.subheader("🏦 Solidità finanziaria")
        st.write(f"- **Capacità di autofinanziamento:** {gpt_result['autofinanziamento']}")
        st.write(f"- **Disponibilità liquide:** {gpt_result['disponibilità_liquide']}")
        st.write(f"- **Indebitamento:** {gpt_result['indebitamento']}")
        st.info(gpt_result["solidità_finanziaria"])

        st.subheader("💸 Redditività")
        st.metric("Utile Netto", f"€ {azienda_data['utile_netto']:,}")
        st.metric("EBITDA", f"€ {azienda_data['ebitda']:,}")
        st.info(gpt_result["redditività"])

        st.subheader("🧪 Investimenti recenti")
        st.write(f"- **Beni strumentali:** € {azienda_data['beni_strumentali']:,}")
        st.write(f"- **R&S:** € {azienda_data['ricerca_sviluppo']:,}")
        st.info(gpt_result["investimenti"])

        st.subheader("🏢 Altri dati aziendali")
        st.write(f"- **Codice ATECO:** {azienda_data['codice_ateco']}")
        st.write(f"- **Sede legale:** {azienda_data['sede_legale']}")
        st.write(f"- **Data di costituzione:** {azienda_data['data_costituzione']}")

        st.subheader("🧾 Valutazione complessiva")
        st.success(f"**Voto generale:** {gpt_result['voto_finale']} – {gpt_result['commento_generale']}")

        st.header("🏛️ Analisi Opportunità Finanziamento")
        st.info("Recupero bandi aggiornati da Supabase...")
        bandi_testo = fetch_bandi()

        st.info("Matching con bandi in corso...")
        claude_result = match_with_bandi(azienda_data, gpt_result, bandi_testo)

        st.subheader("📌 Bandi compatibili")
        for bando in claude_result["bandi_compatibili"]:
            st.markdown(f"**{bando['titolo']}** – Score: {bando['score']}<br>{bando['motivazione']}", unsafe_allow_html=True)

        st.subheader("🚦 Compatibilità requisiti")
        st.json(claude_result["criteri_compatibilità"])

        st.subheader("📝 Relazione conclusiva")
        st.markdown(f"> {claude_result['commento_generale']}")
