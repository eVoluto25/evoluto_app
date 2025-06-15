import os

# Claude API key
CLAUDE_KEY = os.getenv("CLAUDE_KEY")

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Porta per uvicorn (default 8000)
PORT = int(os.getenv("PORT", 8000))
