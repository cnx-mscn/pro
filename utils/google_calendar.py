
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "google/calendar_credentials.json"
CALENDAR_ID = "primary"

def add_event_to_calendar(summary, description, date):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("calendar", "v3", credentials=credentials)

    event = {
        "summary": summary,
        "description": description,
        "start": {"date": str(date), "timeZone": "Europe/Istanbul"},
        "end": {"date": str(date), "timeZone": "Europe/Istanbul"}
    }

    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event.get("htmlLink")
