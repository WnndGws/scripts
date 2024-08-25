#!/usr/bin/env python
# Remind me about sport over night.

"""Useful modules:
* "addict" for dictionaries
* "alive-progress" for progress bars
* "arrow" for datetime
* "birdseye" for debugging
* "decorator" for humans
* "httpx" for requests
* "plumbum" for shell commands
* "questionary" for user prompts
* "tanacity" for retries
* "ultrajson" for json
* anybadge
* click
* configparser
* humanise
* loguru
* pathlib
* regex
* rich
* schedule
* thefuzz
* tinydb
"""

import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds_path = f"{Path.home()}/.cache/credentials"


def check_calendar(url):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if Path.exists(f"{creds_path}/sport_reminder.json"):
        creds = Credentials.from_authorized_user_file(
            f"{creds_path}/sport_reminder.json", SCOPES
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f"{creds_path}/sport_reminder_credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f"{creds_path}/sport_reminder.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


def main():
    pass


if __name__ == "__main__":
    main()
