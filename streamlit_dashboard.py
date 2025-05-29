
import streamlit as st
import plotly.graph_objects as go

# Configurazione base della pagina
st.set_page_config(layout="wide", page_title="Cruscotto Analisi Finanziaria", page_icon="📊")

# Stile personalizzato
st.markdown("""
    <style>
        .main {
            background-color: #d3d3d3;
            font-family: 'Orbitron', sans-serif;
        }
        .metric-box {
            border-radius: 10px;
            background-color: ivory;
            padding: 20px;
            margin: 10px;
            box-shadow: 4px 4px 10px rgba(0,0,0,0.2);
        }
        .header-metric {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .value-metric {
            font-size: 28px;
            color: black;
        }
        .bando-box {
            background-color: black;
            color: ivory;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .gauge-title {
            font-size: 18px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Layout superiore: 2 gauge circolari per ICR e Debt/Equity
col1, col2 = st.columns(2)

with col1:
    fig_icr = go.Figure(go.Indicator(
        mode="gauge+number",
        value=2.8,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Interest Coverage Ratio (ICR)", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 5]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 1], 'color': "red"},
                {'range': [1, 3], 'color': "yellow"},
                {'range': [3, 5], 'color': "green"}
            ]
        }
    ))
    st.plotly_chart(fig_icr, use_container_width=True)

with col2:
    fig_debt = go.Figure(go.Indicator(
        mode="gauge+number",
        value=58,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Rapporto Indebitamento (%)", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 40], 'color': "green"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ]
        }
    ))
    st.plotly_chart(fig_debt, use_container_width=True)

# Riquadri centrali: numero bandi e punteggio compatibilità
st.markdown('<div class="bando-box">Bandi disponibili: 12</div>', unsafe_allow_html=True)
st.markdown('<div class="bando-box" style="color: lime;">Compatibilità media: 8.6 / 10</div>', unsafe_allow_html=True)

# Layout inferiore: 2 gauge semicircolari per Liquidità e Utile Netto
col3, col4 = st.columns(2)

with col3:
    fig_liq = go.Figure(go.Indicator(
        mode="gauge+number",
        value=72,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Liquidità Aziendale (€000)", 'font': {'size': 20}},
        gauge={
            'shape': "angular",
            'axis': {'range': [0, 100]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "green"}
            ]
        }
    ))
    st.plotly_chart(fig_liq, use_container_width=True)

with col4:
    fig_utile = go.Figure(go.Indicator(
        mode="gauge+number",
        value=64,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Utile Netto (€000)", 'font': {'size': 20}},
        gauge={
            'shape': "angular",
            'axis': {'range': [0, 100]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "green"}
            ]
        }
    ))
    st.plotly_chart(fig_utile, use_container_width=True)
