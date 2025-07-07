from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPES = ["https://www.googleapis.com/auth/calendar"]

router = APIRouter()

# 🔵 In-memory storage token (esempio, poi metti in DB sicuro)
USER_TOKENS = {}

# 1️⃣ Avvio autorizzazione
@router.get("/authorize")
async def authorize(user_id: str):
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

# 2️⃣ Ricezione codice OAuth
@router.get("/oauth2callback")
async def oauth2callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

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

    # Qui user_id è da gestire come parametro reale o cookie
    user_id = "demo_user"
    USER_TOKENS[user_id] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }

    return JSONResponse({"message": "Autenticazione completata."})

# 3️⃣ Leggi disponibilità
@router.post("/availability")
async def get_calendar_availability(data: dict):
    user_id = data.get("user_id", "demo_user")
    start = data["start_date"]
    end = data["end_date"]

    if user_id not in USER_TOKENS:
        raise HTTPException(status_code=401, detail="Token non trovato. Esegui /authorize.")

    creds = Credentials(**USER_TOKENS[user_id])

    service = build("calendar", "v3", credentials=creds)
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    return {"events": events}

# 4️⃣ Crea evento con link Meet
@router.post("/create_event")
async def create_calendar_event(data: dict):
    user_id = data.get("user_id", "demo_user")
    if user_id not in USER_TOKENS:
        raise HTTPException(status_code=401, detail="Token non trovato. Esegui /authorize.")

    creds = Credentials(**USER_TOKENS[user_id])
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": data["title"],
        "description": data.get("description", ""),
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

    return {"event": created_event}
