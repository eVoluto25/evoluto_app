import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta

# Configurazione utenti
users = {
    "admin": {
        "name": "Admin User",
        "password": stauth.Hasher(["admin_password"]).generate()[0],
        "role": "admin"
    },
    "cliente1": {
        "name": "Cliente 1",
        "password": stauth.Hasher(["cliente_password"]).generate()[0],
        "role": "cliente"
    }
}

# Config YAML simulato
config = {
    'credentials': {
        'usernames': {
            username: {
                'name': data['name'],
                'password': data['password']
            } for username, data in users.items()
        }
    },
    'cookie': {
        'expiry_days': 0,
        'key': 'random_cookie_key',
        'name': 'streamlit_auth'
    },
    'preauthorized': {}
}

# Autenticazione
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login("Login", "main")

# Timeout della sessione
if 'session_start_time' not in st.session_state:
    st.session_state.session_start_time = datetime.now()
else:
    if datetime.now() - st.session_state.session_start_time > timedelta(minutes=30):
        st.warning("Sessione scaduta. Effettua di nuovo il login.")
        authenticator.logout("Logout", "sidebar")
        st.stop()

# Autenticazione riuscita
if authentication_status:
    role = users[username]["role"]
    st.session_state["username"] = username
    st.session_state["role"] = role
    authenticator.logout("Logout", "sidebar")
    st.success(f"Benvenuto {name} ({role})")

# Errore di login
elif authentication_status is False:
    st.error("Username o password errati")

# In attesa di inserimento credenziali
elif authentication_status is None:
    st.info("Inserisci username e password")
