
import streamlit_authenticator as stauth

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
