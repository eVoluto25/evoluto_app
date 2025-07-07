from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
import pytz
import os
from supabase import create_client

router = APIRouter()

# 🔹 Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 Variabili ambiente Google
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# 🔹 Recupera credenziali da Supabase
def get_credentials_from_supabase():
    user_id = "mio_calendario"
    res = supabase.table("calendar_tokens").select("*").eq("user_id", user_id).single().execute()
    data = res.data
    if not data:
        raise HTTPException(status_code=401, detail="Token non trovato. Devi autorizzare prima.")
    return Credentials(
        token=data["access_token"],
        refresh_token=data["refresh_token"],
        token_uri=data["token_uri"],
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        scopes=SCOPES
    )

# 🔹 Endpoint per avviare autorizzazione
@router.get("/authorize")
async def authorize():
    flow = Flow.from_client_config(
        {
            "web": {
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

# 🔹 Callback per salvare token
@router.get("/oauth2callback")
async def oauth2callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Codice OAuth mancante.")

    flow = Flow.from_client_config(
        {
            "web": {
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

    data = {
        "user_id": "mio_calendario",
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": ",".join(creds.scopes or [])
    }

    clean_data = {k: v for k, v in data.items() if v is not None}

    supabase.table("calendar_tokens").upsert(clean_data).execute()

    return JSONResponse({"message": "Token salvato su Supabase."})

# 🔹 Calcola fasce disponibili Martedì/Giovedì 9–12
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

# 🔹 Recupera disponibilità settimana corrente e prossima
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

# 🔹 Modello per creazione evento
class EventoInput(BaseModel):
    nome: str
    cognome: str
    telefono: str
    email: EmailStr
    start_time: str
    end_time: str
    ragione_sociale: str
    obiettivo_preferenziale: str

# 🔹 Crea evento sul calendario con descrizione automatica
@router.post("/create_event")
async def create_calendar_event(data: EventoInput):
    creds = get_credentials_from_supabase()
    service = build("calendar", "v3", credentials=creds)

    start_dt = datetime.fromisoformat(data.start_time)
    data_str = start_dt.strftime("%d/%m/%Y")
    ora_str = start_dt.strftime("%H:%M")

    descrizione = (
        f"Consulenza specialistica con {data.nome} {data.cognome}\n"
        f"Giorno e ora: {data_str} ore {ora_str}\n"
        f"Telefono: {data.telefono}\n"
        f"Email: {data.email}"
        f"Azienda: {data.ragione_sociale}\n"
        f"Obiettivo: {data.obiettivo_preferenziale}"
    )

    event = {
        "summary": f"Consulenza con {data.nome} {data.cognome}",
        "description": descrizione,
        "start": {"dateTime": data.start_time, "timeZone": "Europe/Rome"},
        "end": {"dateTime": data.end_time, "timeZone": "Europe/Rome"},
        "conferenceData": {
            "createRequest": {
                "requestId": f"evoluto-meeting-{data.nome}-{data.cognome}",
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
