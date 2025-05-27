
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Section: Dashboard Title
st.markdown("## 📊 Dossier di Verifica Aziendale")
st.markdown("Benvenuto nel cruscotto. Carica i documenti per iniziare l’analisi.")
st.markdown("---")

# Section: Fondi e Valori Economici
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 Totale Fondi Attivi", "€0")
col2.metric("📊 Fondi Compatibili", "€0", delta_color="normal")
col3.metric("🎯 Probabilità Media di Successo", "ND")
col4.metric("🏢 Fatturato Annuo", "€0")
col5.metric("📋 Totale Attivo di Bilancio", "€0")
st.markdown("---")

# Section: Indicatori Finanziari Chiave (Piramide)
st.markdown("### 📈 Indicatori Finanziari Chiave")
upper1, upper2 = st.columns(2)
lower1, lower2, lower3 = st.columns(3)

def draw_gauge(title):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 0,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#6c757d"},
            'bgcolor': "#e9ecef",
            'borderwidth': 1,
        }
    ))
    fig.update_layout(height=220, margin=dict(t=30, b=0, l=10, r=10))
    return fig

with upper1:
    st.plotly_chart(draw_gauge("Capacità di autofinanziamento"), use_container_width=True)
with upper2:
    st.plotly_chart(draw_gauge("Disponibilità liquide"), use_container_width=True)
with lower1:
    st.plotly_chart(draw_gauge("Indebitamento"), use_container_width=True)
with lower2:
    st.plotly_chart(draw_gauge("Utile netto"), use_container_width=True)
with lower3:
    st.plotly_chart(draw_gauge("EBITDA"), use_container_width=True)

st.markdown("---")

# Section: Anagrafica Aziendale (Static Box)
st.markdown("### 🏷️ Anagrafica Aziendale")
with st.container():
    col1, col2, col3 = st.columns(3)
    col1.markdown("**📛 Ragione Sociale:** Azienda SRL")
    col2.markdown("**🏙️ Provincia:** MI")
    col3.markdown("**📅 Anno di Fondazione:** 2000")
    col1.markdown("**👥 Dipendenti:** 25")
    col2.markdown("**📞 Contatto:** info@azienda.it")
    col3.markdown("**🔢 Partita IVA:** 12345678901")
