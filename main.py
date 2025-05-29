
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from config import CONFIG
from datetime import timedelta
from dashboard_components import render_dashboard
from secure_file_handler import handle_uploaded_files

# --- Autenticazione ---
with open('config_auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f"Benvenuto **{name}** 👋")

    # Titolo Dashboard
    st.title("🛡️ Cruscotto Analisi Aziendale – eVoluto")

    # Upload file (solo admin)
    if username == "admin":
        uploaded_files = st.file_uploader("Carica documenti aziendali (PDF visura, XBRL bilancio)", type=['pdf', 'xbrl'], accept_multiple_files=True)
        if uploaded_files:
            handle_uploaded_files(uploaded_files)

    # Layout dashboard
    render_dashboard()

elif authentication_status is False:
    st.error("Username o password non corretti.")
elif authentication_status is None:
    st.warning("Inserisci le credenziali per accedere.")
