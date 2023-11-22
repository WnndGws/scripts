#!/usr/bin/env python3
"""
Ban succesful resposters on reddit
"""
import configparser

import praw

CONFIG = configparser.ConfigParser()
FILEDIR = "/home/wynand/.cache/credentials"
CONFIG.read(f"{FILEDIR}/reddit.ini")

USER = CONFIG["SETTINGS"]["username"]
PW = CONFIG["SETTINGS"]["password"]
ID = CONFIG["SETTINGS"]["client_id"]
SECRET = CONFIG["SETTINGS"]["client_secret"]

reddit = praw.Reddit(
    client_id=ID,
    client_secret=SECRET,
    user_agent="my user agent",  # user agent name
    username=USER,  # your reddit username
    password=PW,  # your reddit password
)


def banspam():
    for post in reddit.subreddit("all").hot(limit=200):
        ck = post.author.comment_karma or 1
        tk = post.author.total_karma
        factor = tk / ck
        if factor > 100 and tk > 10000:
            print(f"Ban {post.author} {factor} {post.title}")
            post.author.block()


if __name__ == "__main__":
    banspam()
