import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta

# Crea hash delle password in chiaro
hashed_passwords = stauth.Hasher(["admin123", "cliente123"]).generate()

# Definizione utenti
users = {
    "admin": {
        "name": "Admin User",
        "password": hashed_passwords[0],
        "role": "admin"
    },
    "cliente1": {
        "name": "Cliente 1",
        "password": hashed_passwords[1],
        "role": "cliente"
    }
}

# Configurazione Streamlit Authenticator
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
        'expiry_days': 1,
        'key': 'evoluto_login_cookie',
        'name': 'evoluto_cookie'
    },
    'preauthorized': {
        'emails': []
    }
}

# Funzione di login
def login_user():
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    name, authentication_status, username = authenticator.login('Login', 'main')
    return authenticator, name, authentication_status, username
