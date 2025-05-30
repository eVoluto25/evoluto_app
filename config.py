import os
from google.oauth2.service_account import Credentials

# ID del foglio Google Sheets
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

# Funzione per ottenere le credenziali Google
def get_google_credentials():
    credentials_info = {
        "type": "service_account",
        "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
        "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.environ.get("GOOGLE_SERVICE_ACCOUNT_EMAIL"),
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "auth_uri": os.environ.get("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
        "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
        "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_CERT_URL"),
        "universe_domain": os.environ.get("GOOGLE_UNIVERSE_DOMAIN", "googleapis.com"),
    }

    return Credentials.from_service_account_info(credentials_info)
