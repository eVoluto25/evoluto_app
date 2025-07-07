from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from datetime import datetime, timedelta
import pytz
import os
from supabase import create_client

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Recupera token da Supabase
def get_credentials_from_supabase():
    user_id = "mio_calendario"
    res = supabase.table("calendar_tokens").select("*").eq("user_id", user_id).single().execute()
    data = res.data
    if not data:
        raise HTTPException(status_code=401, detail="Token non trovato. Esegui autorizzazione iniziale.")
    return Credentials(
        token=data["access_token"],
        refresh_token=data["refresh_token"],
        token_uri=data["token_uri"],
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        scopes=SCOPES
    )

# Avvia autorizzazione
@router.get("/calendar/authorize")
async def authorize():
    flow = Flow.from_client_config(
        {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline", include_granted_scopes="true")
    return JSONResponse({"auth_url": auth_url})

# Salva token in Supabase
@router.get("/calendar/oauth2callback")
async def oauth2callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Codice OAuth mancante.")

    flow = Flow.from_client_config(
        {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(code=code)
    creds = flow.credentials

    supabase.table("calendar_tokens").upsert({
        "user_id": "mio_calendario",
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret
    }).execute()

    return JSONResponse({"message": "Token salvato su Supabase."})

# Recupera disponibilità
@router.get("/calendar/availability")
async def get_calendar_availability():
    creds = get_credentials_from_supabase()
    service = build("calendar", "v3", credentials=creds)

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_next_week = start_of_week + timedelta(days=13)

    start_str = start_of_week.isoformat()
    end_str = end_of_next_week.isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_str + "T00:00:00Z",
        timeMax=end_str + "T23:59:59Z",
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])
    # Calcolo slot (puoi usare la tua funzione)

    return {"fasce_disponibili": []}

# Crea evento
@router.post("/calendar/create_event")
async def create_calendar_event(data: dict):
    creds = get_credentials_from_supabase()
    service = build("calendar", "v3", credentials=creds)
    event = {
        "summary": data["title"],
        "start": {"dateTime": data["start_time"], "timeZone": "Europe/Rome"},
        "end": {"dateTime": data["end_time"], "timeZone": "Europe/Rome"},
        "conferenceData": {
            "createRequest": {
                "requestId": "evoluto-meeting",
                "conferenceSolutionKey": {"type": "hangoutsMeet"}
            }
        }
    }
    created_event = service.events().insert(
        calendarId="primary",
        body=event,
        conferenceDataVersion=1
    ).execute()
    return {"evento_creato": created_event}
