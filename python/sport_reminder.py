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
    APPLICATION_NAME = "Sport Reminder"
    FLAGS = None

    home_dir = Path.home()
    credential_dir = Path.joinpath(home_dir, ".cache/credentials")
    if not Path.exists(credential_dir)
        Path.mkdir(credential_dir)
    credential_path = Path.joinpath(credential_dir,)
    CLIENT_SECRET_FILE = os.path.join(credential_dir, CLIENT_SECRET_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print("Storing credentials to " + credential_path)
    return credentials
