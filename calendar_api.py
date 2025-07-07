from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import pytz
import os

from supabase import create_client

# Configura Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

# 🔹 Recupera sempre il tuo token unico
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
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

# 🔹 Calcola slot disponibili Martedì/Giovedì 9–12
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

# 🔹 Endpoint per disponibilità settimana corrente + prossima
@router.get("/availability")
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
    available_slots = calculate_available_slots(events, start_str, end_str)

    return {"fasce_disponibili": available_slots}

# 🔹 Endpoint per creazione evento
@router.post("/create_event")
async def create_calendar_event(data: dict):
    creds = get_credentials_from_supabase()
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
