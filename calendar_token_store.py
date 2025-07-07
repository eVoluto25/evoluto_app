from supabase import create_client
import os

# Configura client Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "calendar_tokens"

def save_token(user_id: str, token_data: dict):
    """
    Salva o aggiorna i token per un determinato utente.
    """
    # Verifica se esiste già
    existing = (
        supabase
        .from_(TABLE_NAME)
        .select("user_id")
        .eq("user_id", user_id)
        .execute()
    )

    if existing.data:
        # Aggiorna
        supabase
        .from_(TABLE_NAME)
        .update({
            "access_token": token_data["token"],
            "refresh_token": token_data["refresh_token"],
            "token_uri": token_data["token_uri"],
            "client_id": token_data["client_id"],
            "client_secret": token_data["client_secret"],
            "scopes": token_data["scopes"]
        })
        .eq("user_id", user_id)
        .execute()
    else:
        # Inserisci nuovo
        supabase
        .from_(TABLE_NAME)
        .insert({
            "user_id": user_id,
            "access_token": token_data["token"],
            "refresh_token": token_data["refresh_token"],
            "token_uri": token_data["token_uri"],
            "client_id": token_data["client_id"],
            "client_secret": token_data["client_secret"],
            "scopes": token_data["scopes"]
        })
        .execute()

def load_token(user_id: str) -> dict | None:
    """
    Recupera i token per un determinato utente.
    """
    result = (
        supabase
        .from_(TABLE_NAME)
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    if result.data:
        return {
            "token": result.data["access_token"],
            "refresh_token": result.data["refresh_token"],
            "token_uri": result.data["token_uri"],
            "client_id": result.data["client_id"],
            "client_secret": result.data["client_secret"],
            "scopes": result.data["scopes"]
        }
    else:
        return None
