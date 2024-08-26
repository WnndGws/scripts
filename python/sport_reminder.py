#!/usr/bin/env python
# Remind me about sport over night.

"""Useful modules.

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


def get_credentials():
    """Get valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns
    -------
        Credentials, the obtained credential.

    """
    # If modifying these scopes, delete your previously saved credentials
    scopes = "https://www.googleapis.com/auth/calendar"
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


def check_calendar(url) -> list():
    """Check given calendar and return the relevant events."""
    creds = get_credentials()
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


if __name__ == "__main__":
    get_credentials()
