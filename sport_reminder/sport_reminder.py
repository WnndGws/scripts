#!/usr/bin/env -S uv run

from pathlib import Path

import arrow
import ujson
from addict import Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich import print_json

id_list = [
    "ct240d39oc9kq21cq3bn70jii8@group.calendar.google.com",  # International Rugby
    "nba_-m-0jmgb_%4dinnesota+%54imberwolves#sports@group.v.calendar.google.com",  # Timberwolves
    "mlb_-m-0512p_%4dinnesota+%54wins#sports@group.v.calendar.google.com",  # Twins
    "nfl_-m-051q5_%4dinnesota+%56ikings#sports@group.v.calendar.google.com",  # Vikings
    "ijj3danperuqhjfsrtpdq41h2ekqdf84@import.calendar.google.com",  # Sadspurs
]


def get_credentials():
    """Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns
    -------
        Credentials, the obtained credential.

    """
    # If modifying these scopes, delete your previously saved credentials
    scopes = ["https://www.googleapis.com/auth/calendar"]
    client_secrets_file = "sport_reminder_secrets.json"
    client_creds_file = "sport_reminder_credentials.json"
    creds = None

    # Set up locations of files
    home_dir = Path.home()
    credential_dir = Path.joinpath(home_dir, ".cache/credentials")
    if not Path.exists(credential_dir):
        Path.mkdir(credential_dir)
    credential_path = Path.joinpath(credential_dir, client_creds_file)
    secret_path = Path.joinpath(credential_dir, client_secrets_file)

    # If the file exists, then try use it
    if Path.exists(secret_path):
        creds = Credentials.from_authorized_user_file(secret_path, scopes)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_path, scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(secret_path, "w") as token:
            token.write(creds.to_json())

    return creds


def check_calendar(id: str) -> None:
    """Check given calendar and return the relevant events."""
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = arrow.utcnow()
    local = now.to("Australia/Canberra")
    local_later = local.shift(days=31)
    print("Getting any events missed over night")
    events_result = (
        service.events()
        .list(
            calendarId=id,
            timeMin=local,
            timeMax=local_later,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    return events


def add_to_calendar() -> None:
    for id in id_list:
        events = check_calendar(id)
        if events:
            creds = get_credentials()
            service = build("calendar", "v3", credentials=creds)

            # Check what events exist in "Sport Reminder" calendar for today already

            for event in events:
                orig_event = Dict(event)
                new_event = Dict()
                try:
                    orig_start_time = arrow.get(orig_event.start.dateTime)
                    duration = arrow.get(orig_event.end.dateTime) - orig_start_time
                    orig_start_time = orig_start_time.to("Australia/Canberra")

                    # Move to the next available 9am
                    replaced_9am = orig_start_time.replace(hour=10, minute=0)
                    if replaced_9am < orig_start_time:
                        replaced_9am = replaced_9am.shift(days=1)
                    new_end_time = replaced_9am + duration

                    # Format correctly
                    new_event.start.dateTime = replaced_9am.format(
                        "YYYY-MM-DDTHH:mm:ssZ"
                    )
                    new_event.end.dateTime = new_end_time.format("YYYY-MM-DDTHH:mm:ssZ")

                    # Add other missing info
                    new_event.summary = orig_event.summary
                    new_event.location = orig_event.location

                    print(
                        "Getting Events that are already added to the Reminder Calendar"
                    )
                    existing_events = (
                        service.events()
                        .list(
                            calendarId="5a57651064d725d01715c74655bc4647d48cdaff24b205eb958a84563c70de4b@group.calendar.google.com",
                            timeMin=replaced_9am,
                            maxResults=10,
                            singleEvents=True,
                            orderBy="startTime",
                        )
                        .execute()
                    )
                    existing_events = existing_events.get("items", [])

                    # Check if event already exists
                    exist_count = 0
                    for check_event in existing_events:
                        check_event = Dict(check_event)
                        if new_event.summary == check_event.summary:
                            exist_count += 1

                    if exist_count > 0:
                        print("Exists already, passing")
                    else:
                        print("Adding new event...")
                        service.events().insert(
                            calendarId="5a57651064d725d01715c74655bc4647d48cdaff24b205eb958a84563c70de4b@group.calendar.google.com",
                            body=new_event,
                        ).execute()
                except TypeError:
                    print(f"Skipping {orig_event.summary}")
        else:
            print("No events over night")


if __name__ == "__main__":
    add_to_calendar()
