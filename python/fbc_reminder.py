#!/usr/bin/env python3
"""Reminde me each day about my FBC startups"""

import datetime
import logging
import sys

sys.path.insert(0, "/home/wynand/git/neoFrogBox")

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import check_date_range

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


logging.basicConfig(
    level=logging.CRITICAL, format="%(asctime)s - %(levelname)s - %(message)s"
)


def find_times():
    """Find the times i need to add."""
    times = []
    streams = check_date_range.get_fbc_streams(
        datetime.datetime.utcnow(),
        datetime.datetime.utcnow() + datetime.timedelta(days=1),
        True,
        False,
    )
    for stream in streams:
        time = stream["scheduled_start_UTC"]
        time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:00+00:00")
        times.append(time)

    for time in set(times):
        add_to_calendar(time - datetime.timedelta(minutes=30), time)


def add_to_calendar(start, end):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".config/credentials")
    token_file = os.path.join(credential_dir, "fbc_reminder_token.json")
    credentials_file = os.path.join(credential_dir, "fbc_reminder_credentials.json")
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": "FrogBox Match Support",
            "location": "Online",
            "description": "FBC",
            "start": {
                "dateTime": datetime.datetime.strftime(
                    start, "%Y-%m-%dT%H:%M:00+00:00"
                ),
                "timeZone": "Africa/Abidjan",  # In the UTC timezone
            },
            "end": {
                "dateTime": datetime.datetime.strftime(end, "%Y-%m-%dT%H:%M:00+00:00"),
                "timeZone": "Africa/Abidjan",  # In the UTC timezone
            },
        }

        event = service.events().insert(calendarId="primary", body=event).execute()

    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    find_times()
