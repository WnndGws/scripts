#!/usr/bin/env python3
"""
Takes url list and sees if theyre alive, used to test my newsboat urls
"""
# standard imports
import requests

with open("urldata") as f:
    data = f.read().split("\n")

# Remove trailing ,
data = data[:-1]

for url in data:
    try:
        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
            },
            timeout=10,
        )
        if not r.status_code == 200:
            print(f"{url} FAILED with code {r.status_code}")
    except:
        print(f"{url} failed")
