#!/usr/bin/env python3
"""
Just prints the current time in London and Melbourne
"""

import datetime

import pytz

tz_melb = pytz.timezone("Australia/Melbourne")
tz_london = pytz.timezone("Europe/London")

print(
    f'D{datetime.datetime.now(tz=tz_melb).strftime("%H")}h  {datetime.datetime.now(tz=tz_london).strftime("%H")}h',
)
