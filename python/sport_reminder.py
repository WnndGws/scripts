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


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns
    -------
        Credentials, the obtained credential.

    """
    # If modifying these scopes, delete your previously saved credentials
    SCOPES = "https://www.googleapis.com/auth/calendar"
    CLIENT_SECRET_FILE = "sport_reminder_secrets.json"
    CLIENT_CREDENTIALS_FILE = "sport_reminder_credentials.json"
    creds = None

    # Set up locations of files
    home_dir = Path.home()
    credential_dir = Path.joinpath(home_dir, ".cache/credentials")
    if not Path.exists(credential_dir):
        Path.mkdir(credential_dir)
    credential_path = Path.joinpath(credential_dir, CLIENT_CREDENTIALS_FILE)
    secret_path = Path.joinpath(credential_dir, CLIENT_SECRET_FILE)

    # If the file exists, then try use it
    if Path.exists(secret_path):
        creds = Credentials.from_authorized_user_file(secret_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(secret_path, "w") as token:
            token.write(creds.to_json())


if __name__ == "__main__":
    get_credentials()
