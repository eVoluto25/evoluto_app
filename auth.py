
import streamlit as st
from supabase import create_client, Client
import datetime

# Inizializzazione Supabase
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

def admin_login():
    st.subheader("Accesso Amministratore")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login Admin"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state["user"] = user
            st.session_state["role"] = "admin"
            st.session_state["last_activity"] = datetime.datetime.now()
            st.success("Accesso effettuato come amministratore.")
        except Exception as e:
            st.error("Credenziali non valide.")

def client_login():
    st.subheader("Accesso Cliente")
    email = st.text_input("Email")
    if st.button("Invia OTP"):
        try:
            supabase.auth.sign_in_with_otp({"email": email})
            st.session_state["email"] = email
            st.session_state["otp_sent"] = True
            st.success("OTP inviato all'email fornita.")
        except Exception as e:
            st.error("Errore nell'invio dell'OTP.")
    if st.session_state.get("otp_sent"):
        otp = st.text_input("Inserisci OTP")
        if st.button("Verifica OTP"):
            try:
                user = supabase.auth.verify_otp({"email": st.session_state["email"], "token": otp, "type": "email"})
                st.session_state["user"] = user
                st.session_state["role"] = "cliente"
                st.session_state["last_activity"] = datetime.datetime.now()
                st.success("Accesso effettuato come cliente.")
            except Exception as e:
                st.error("OTP non valido.")

def check_session_timeout():
    if "last_activity" in st.session_state and st.session_state.get("role") == "cliente":
        now = datetime.datetime.now()
        if (now - st.session_state["last_activity"]).seconds > 1800:
            st.warning("Sessione scaduta. Effettua nuovamente l'accesso.")
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
        else:
            st.session_state["last_activity"] = now

def main_auth():
    if "user" not in st.session_state:
        role = st.radio("Seleziona il tipo di accesso", ("Amministratore", "Cliente"))
        if role == "Amministratore":
            admin_login()
        else:
            client_login()
    else:
        check_session_timeout()
        st.write(f"Benvenuto, {st.session_state['role']}")

if __name__ == "__main__":
    main_auth()
