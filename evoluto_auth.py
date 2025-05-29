import streamlit as st

# Dizionario utenti: username -> (password, ruolo)
USER_CREDENTIALS = {
    "admin": ("admin123", "admin"),
    "cliente1": ("cliente123", "cliente")
}

def login_user():
    st.sidebar.subheader("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username][0] == password:
            st.session_state["username"] = username
            st.session_state["role"] = USER_CREDENTIALS[username][1]
            st.session_state["authenticated"] = True
            st.success(f"Benvenuto, {username}!")
            return True, username
        else:
            st.error("Credenziali non valide")
            return False, None

    return st.session_state.get("authenticated", False), st.session_state.get("username", None)
