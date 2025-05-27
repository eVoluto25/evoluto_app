
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Imposta pagina
st.set_page_config(page_title="eVoluto - Cruscotto Aziendale", layout="wide")

# HEADER
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>💼 Dossier di Verifica Aziendale</h1>", unsafe_allow_html=True)
st.markdown("### Benvenuto nel cruscotto. Carica i documenti per iniziare l’analisi.")

# LAYOUT SEZIONE TOP
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("**💰 Totale Fondi Attivi**")
    st.markdown("<h2 style='color:#2980b9;'>€0</h2>", unsafe_allow_html=True)

with col2:
    st.markdown("**📊 Fondi Compatibili**")
    st.markdown("<h2 style='color:#27ae60;'>€0</h2>", unsafe_allow_html=True)

with col3:
    st.markdown("**🎯 Probabilità Media di Successo**")
    st.markdown("<h2 style='color:#f39c12;'>ND</h2>", unsafe_allow_html=True)

with col4:
    st.markdown("**🏢 Fatturato Annuo**")
    st.markdown("<h2 style='color:#8e44ad;'>€0</h2>", unsafe_allow_html=True)

with col5:
    st.markdown("**📋 Totale Attivo di Bilancio**")
    st.markdown("<h2 style='color:#34495e;'>€0</h2>", unsafe_allow_html=True)

# INDICATORI FINANZIARI
st.markdown("---")
st.markdown("### 📈 Indicatori Finanziari Chiave")

labels = ["Capacità di autofinanziamento", "Disponibilità liquide", "Indebitamento", "Utile netto", "EBITDA"]
values = [0, 0, 0, 0, 0]

rows = 1
cols = len(labels)

fig = make_subplots(rows=1, cols=5, specs=[[{'type': 'indicator'}]*5])
colors = ['#3498db', '#1abc9c', '#e74c3c', '#9b59b6', '#f1c40f']

for i, (label, value, color) in enumerate(zip(labels, values, colors)):
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label, 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'bgcolor': "#ecf0f1"
        }
    ), row=1, col=i+1)

fig.update_layout(height=300, margin=dict(t=30, b=0, l=0, r=0))

st.plotly_chart(fig, use_container_width=True)

# 🧾 Informazioni Anagrafiche Aziendali
st.markdown("---")
st.markdown("### 🧾 Informazioni Anagrafiche Aziendali")
with st.container():
    st.markdown("**Ragione Sociale:** ND")
    st.markdown("**Partita IVA:** ND")
    st.markdown("**Codice Fiscale:** ND")
    st.markdown("**Sede Legale:** ND")
    st.markdown("**Codice ATECO:** ND")
