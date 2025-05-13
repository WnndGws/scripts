#!/usr/bin/env -S uv run
"""Checks Google Calendar for next event and displays it nicely."""

from pathlib import Path

import arrow
import regex
import ujson
from addict import Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich import print_json

# python-oauth2client
# python-google-api-python-client

id_list = [
    "5a57651064d725d01715c74655bc4647d48cdaff24b205eb958a84563c70de4b@group.calendar.google.com",  # Sport Reminder
    "primary",  # Personal Calendar
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
    scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
    client_secrets_file = "next_event_secrets.json"
    client_creds_file = "next_event_credentials.json"
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
    local_later = local.shift(days=+2)
    local = local.shift(days=-1)
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


def truncate_fstring(s: str, max_length: int = 20) -> str:
    return s if len(s) <= max_length else s[: max_length - 3] + "..."


def main():
    now = arrow.utcnow()
    local_time = now.to("Australia/Canberra")

    all_events = []
    for id in id_list:
        events = check_calendar(id)
        if events:
            for event in events:
                all_events.append(event)

        # Split calendar into blocks of time, thus can show past events as 'next' event if there is nothing else on today
        new_events = []
        for i, event in enumerate(all_events):
            new_event = Dict(event)
            try:
                next_event = Dict(events[i + 1])
                new_event.end.adjustedDateTime = next_event.start.dateTime
            except IndexError:
                try:
                    new_event.end.adjustedDateTime = arrow.get(
                        new_event.end.dateTime
                    ).replace(hour=4, minute=0, second=0, microsecond=0)
                    if new_event.end.adjustedDateTime < arrow.get(
                        new_event.start.dateTime
                    ):
                        end_time = new_event.end.adjustedDateTime.shift(days=+1)
                    else:
                        end_time = new_event.end.adjustedDateTime
                    new_event.end.adjustedDateTime = end_time.isoformat()
                except TypeError:
                    new_event.allDay = True
                    new_event.start.dateTime = f"{new_event.start.date}T00:00:00+10:00"
                    new_event.end.dateTime = f"{new_event.end.date}T00:00:00+10:00"

            new_events.append(new_event)

    # Sort new_events by start time
    new_events = sorted(new_events, key=lambda x: x.start.dateTime)

    # Check if time now matches any event time
    current_event = next(
        (
            event
            for event in new_events
            if arrow.get(event.start.dateTime)
            <= local_time
            <= arrow.get(event.end.dateTime)
        ),
        None,
    )

    adjusted_event = next(
        (
            event
            for event in new_events
            if arrow.get(event.start.dateTime)
            <= local_time
            <= arrow.get(event.end.adjustedDateTime)
        ),
        None,
    )

    next_event = next(
        (
            event
            for event in new_events
            if local_time <= arrow.get(event.start.dateTime)
        ),
        None,
    )

    all_day_event = next(
        (
            event
            for event in new_events
            if (
                (local_time.date() == arrow.get(event.start.dateTime).date())
                and event.all_day_event
            )
        ),
        None,
    )

    pattern = regex.compile(r"T(\d{2}:\d{2}):\d{2}")

    if current_event:
        print_now = f"NOW-{current_event.summary.replace(' @ ', '@')}"
    elif adjusted_event:
        time = pattern.search(adjusted_event.start.dateTime)
        print_now = truncate_fstring(
            f"ADJ@{time.group(1)}-{adjusted_event.summary.replace(' @ ', '@')}"
        )
    elif all_day_event:
        print_now = f"ALL DAY-{all_day_event.summary.replace(' @ ', '@')}"
    else:
        print_now = "Nothing missed"

    if next_event:
        time = pattern.search(next_event.start.dateTime)
        print_next = truncate_fstring(
            f"NEXT@{time.group(1)}-{next_event.summary.replace(' @ ', '@')}"
        )
    else:
        print_next = "Nothing upcoming"

    print(f"{print_now} || {print_next}")


if __name__ == "__main__":
    main()
