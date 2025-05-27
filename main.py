
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# === Placeholder for analysis check ===
analisi_completata = False

# === Stile generale ===
st.set_page_config(page_title="Cruscotto Aziendale", layout="wide")

# === TITOLO ===
st.title("💼 Dossier di Verifica Aziendale")
st.write("Benvenuto nel cruscotto. Carica i documenti per iniziare l’analisi.")

# === NAVIGAZIONE ===
with st.sidebar:
    st.markdown("## Navigazione")
    if st.button("Cruscotto"):
        st.switch_page("main.py")
    if st.button("Elenco Bandi"):
        st.switch_page("pagine/1_elenco_bandi.py")
    if st.button("Relazioni AI"):
        st.switch_page("pagine/2_relazioni_ai.py")
    if st.button("Carica Documenti"):
        st.switch_page("pagine/3_carica_documenti.py")

# === 1. FONDI DISPONIBILI ===
st.markdown("## 💰 Risorse ancora disponibili per la Tua Azienda")

col1, col2, col3 = st.columns(3)
col1.metric("Totale Fondi Attivi", "€0" if not analisi_completata else "€850M")
col2.metric("Fondi Compatibili", "€0" if not analisi_completata else "€230K")
col3.metric("Probabilità Media di Successo", "ND" if not analisi_completata else "78.3%")

st.info("⚠️ Carica i documenti per visualizzare l’analisi e i grafici relativi ai bandi disponibili.")

# === 2. INDICATORI FINANZIARI CHIAVE ===
st.markdown("## 📉 Indicatori Finanziari Chiave")

labels = [
    "Capacità di autofinanziamento", "Disponibilità liquide", "Indebitamento",
    "Utile netto", "EBITDA"
]
valori = [0, 0, 0, 0, 0] if not analisi_completata else [68, 54, 35, 70, 60]

fig = make_subplots(
    rows=2, cols=3,
    specs=[[{'type':'indicator'}]*3, [{'type':'indicator'}]*3],
    subplot_titles=labels
)

for i, val in enumerate(valori):
    row = i // 3 + 1
    col = i % 3 + 1
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=val,
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "gray"}},
        number={'font': {'size': 28}},
        domain={'row': row-1, 'column': col-1}
    ), row=row, col=col)

fig.update_layout(height=450, margin=dict(t=30, b=10), showlegend=False)
st.plotly_chart(fig, use_container_width=True)
