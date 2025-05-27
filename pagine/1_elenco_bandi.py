
import streamlit as st

st.title("📄 Elenco Bandi Disponibili")
st.write("Qui sarà mostrato l’elenco dei bandi più rilevanti per l’azienda.")


import streamlit as st

st.sidebar.markdown("## Navigazione")
if st.sidebar.button("Cruscotto"):
    st.switch_page("main.py")
if st.sidebar.button("Elenco Bandi"):
    st.switch_page("pages/1_elenco_bandi.py")
if st.sidebar.button("Relazioni AI"):
    st.switch_page("pages/2_relazioni_ai.py")
if st.sidebar.button("Carica Documenti"):
    st.switch_page("pages/3_carica_documenti.py")

