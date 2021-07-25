"""get-calendar-events.py

A script that gets the calendar events for the user associated with the token.
"""

from datetime import datetime
from datetime import time
from datetime import timedelta

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


API_SERVICE_NAME = "calendar"
API_VERSION = "v3"

TOKEN_FILE = "token.json"

EVENT_TIME_FORMAT_CODE = "%I:%M %p"


def get_calendar_events_for_the_rest_of_today():
    credentials = Credentials.from_authorized_user_file(TOKEN_FILE)

    # If the credentials have expired, we should refresh them.
    if credentials.expired:
        credentials.refresh(Request())

        with open(TOKEN_FILE, "w") as token_file:
            token_file.write(credentials.to_json())

    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    tzinfo = datetime.now().astimezone().tzinfo
    now = datetime.now(tzinfo)
    end_of_day = datetime.combine(now.date(), time(), tzinfo) + timedelta(days=1)

    page_token = None
    while True:
        events = (
            service.events()
            .list(
                calendarId="primary",
                orderBy="startTime",
                pageToken=page_token,
                singleEvents=True,
                timeMin=f"{now.isoformat()}",
                timeMax=f"{end_of_day.isoformat()}",
            )
            .execute()
        )

        for event in events["items"]:
            event_start = datetime.fromisoformat(event["start"]["dateTime"])
            event_end = datetime.fromisoformat(event["end"]["dateTime"])

            print(
                f"[{event_start.strftime(EVENT_TIME_FORMAT_CODE)} - {event_end.strftime(EVENT_TIME_FORMAT_CODE)}] {event['summary']}"
            )

        page_token = events.get("nextPageToken")
        if not page_token:
            break


if __name__ == "__main__":
    get_calendar_events_for_the_rest_of_today()
