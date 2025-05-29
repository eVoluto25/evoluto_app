
# config.py – Centralizzazione delle costanti per il progetto eVoluto

# === Scoring e Classificazione Macro Aree ===
THRESHOLDS = {
    "current_ratio": 1.0,
    "debt_equity_high": 2.0,
    "debt_equity_low": 0.5,
    "ebitda_margin_low": 5.0,
    "ebitda_margin_medium": 10.0,
    "ebitda_margin_high": 15.0,
}

# === Scoring Bandi ===
SCORING_WEIGHTS = {
    "solidita_finanziaria": 0.4,
    "compatibilita_macro_area": 0.3,
    "dimensioni_impresa": 0.3
}

SCORING_CLASSIFICATION = {
    "alta": 80,
    "media": 50,
    "bassa": 0
}

# === File e Sicurezza ===
TEMP_STORAGE_PATH = "/tmp/evoluto_uploads"
KEY_EXPIRATION_MINUTES = 10
MAX_FILE_SIZE_MB = 10

# === Cruscotto Streamlit ===
DEFAULT_ANALYSIS_TIMEOUT_MIN = 30
USER_SESSION_TIMEOUT_MIN = 30

# === Supabase / Storage ===
SUPABASE_ANALYSIS_FOLDER = "analisi_clienti"
SUPABASE_KEY_FIELD = "user_id"

# === Log e Audit ===
LOG_LEVEL = "INFO"
LOG_FILE_PATH = "logs/evoluto_audit.log"
