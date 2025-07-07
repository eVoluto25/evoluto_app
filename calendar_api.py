from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timedelta, time
import pytz
import os

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPES = ["https://www.googleapis.com/auth/calendar"]

router = APIRouter()

# In-memory storage token (esempio)
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
    auth_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="true"
    )
    return JSONResponse({"auth_url": auth_url})

# 2️⃣ Ricezione codice OAuth
@router.get("/oauth2callback")
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

# 3️⃣ Calcola slot liberi Martedì/Giovedì 9–12, in italiano
def calculate_available_slots(events, start_date, end_date, timezone_str="Europe/Rome"):
    tz = pytz.timezone(timezone_str)
    start_dt = tz.localize(datetime.strptime(start_date, "%Y-%m-%d"))
    end_dt = tz.localize(datetime.strptime(end_date, "%Y-%m-%d"))

    busy_slots = []
    for e in events:
        busy_slots.append((
            datetime.fromisoformat(e["start"]["dateTime"]).astimezone(tz),
            datetime.fromisoformat(e["end"]["dateTime"]).astimezone(tz)
        ))

    valid_weekdays = [1, 3]  # Martedì=1, Giovedì=3
    available_slots = []

    curr_day = start_dt
    while curr_day <= end_dt:
        if curr_day.weekday() in valid_weekdays:
            # Fascia 9–12
            slot_start = curr_day.replace(hour=9, minute=0, second=0, microsecond=0)
            slot_end = curr_day.replace(hour=12, minute=0, second=0, microsecond=0)

            slot = slot_start
            while slot + timedelta(hours=1) <= slot_end:
                proposed_start = slot
                proposed_end = slot + timedelta(hours=1)

                overlapping = False
                for busy_start, busy_end in busy_slots:
                    if proposed_start < busy_end and proposed_end > busy_start:
                        overlapping = True
                        break

                if not overlapping:
                    # Aggiungi descrizione in italiano
                    available_slots.append({
                        "data": proposed_start.strftime("%d/%m/%Y"),
                        "giorno": proposed_start.strftime("%A"),
                        "ora_inizio": proposed_start.strftime("%H:%M"),
                        "ora_fine": proposed_end.strftime("%H:%M"),
                        "start_iso": proposed_start.isoformat(),
                        "end_iso": proposed_end.isoformat()
                    })

                slot += timedelta(hours=1)

        curr_day += timedelta(days=1)

    return available_slots

# 4️⃣ Endpoint per disponibilità filtrata (settimana corrente + successiva)
@router.get("/availability")
async def get_calendar_availability(user_id: str = "demo_user"):
    # Calcola intervallo settimana corrente e successiva
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_next_week = start_of_week + timedelta(days=13)

    start_str = start_of_week.isoformat()
    end_str = end_of_next_week.isoformat()

    if user_id not in USER_TOKENS:
        raise HTTPException(status_code=401, detail="Token non trovato. Esegui /authorize.")

    creds = Credentials(**USER_TOKENS[user_id])
    service = build("calendar", "v3", credentials=creds)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_str + "T00:00:00Z",
        timeMax=end_str + "T23:59:59Z",
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    available_slots = calculate_available_slots(events, start_str, end_str)

    return {"fasce_disponibili": available_slots}

# 5️⃣ Crea evento con link Meet
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

    return {"evento_creato": created_event}

# 6️⃣ Endpoint test Supabase per verificare connessione e query
@router.get("/test-supabase")
async def test_supabase():
    from supabase import create_client
    import os

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    res = supabase.table("calendar_tokens").select("*").execute()

    return {"dati_calendar_tokens": res.data}
