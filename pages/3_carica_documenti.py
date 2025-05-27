import streamlit as st

st.set_page_config(page_title="Caricamento Documenti", page_icon="📂")

st.title("📂 Caricamento Documenti Aziendali")
st.write("Carica i documenti necessari per avviare l’analisi.")

tipo_upload = st.radio("📑 Scegli come vuoi caricare i documenti:", 
                       ("File unico (Visura + Bilancio formato XBRL)", "Due file separati"))

if tipo_upload == "File unico (Visura + Bilancio formato XBRL)":
    file_unico = st.file_uploader("📄 Carica il Documento Unico (PDF)", type=["pdf"])
else:
    visura = st.file_uploader("📄 Carica la Visura Camerale (PDF)", type=["pdf"])
    bilancio = st.file_uploader("📄 Carica il Bilancio (PDF)", type=["pdf"])
