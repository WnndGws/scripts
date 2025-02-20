import configparser
import math
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode

import httpx
import orjson
import questionary
import typer
from loguru import logger
from pydantic import BaseModel
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from tenacity import retry, stop_after_attempt, wait_exponential
from thefuzz import fuzz, process
from tinydb import Query, TinyDB

app = typer.Typer()
console = Console()

# Configuration and Token Files
CONFIG_FILE = Path("config.ini")
TOKEN_FILE = Path("token.json")
CACHE_FILE = Path("video_cache.json")

# OAuth and API Endpoints
SCOPES = ["https://www.googleapis.com/auth/youtube"]
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

TOKEN_URL = "https://oauth2.googleapis.com/token"
API_BASE_URL = "https://www.googleapis.com/youtube/v3"


class Config(BaseModel):
    client_id: str
    client_secret: str
    source_playlist_ids: list[str]
    target_playlist_id: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int = 3600
    refresh_token: Optional[str] = None

    expiry_time: float = 0

    @classmethod
    def from_dict(cls, data: dict):
        # Calculate expiry time when creating token
        data["expiry_time"] = time.time() + data.get("expires_in", 3600)
        return cls(**data)

    def is_expired(self) -> bool:
        # Add 60-second buffer before expiration
        return time.time() >= (self.expiry_time - 60)

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "expiry_time": self.expiry_time,
        }


def save_token(token: Token, path: Path = Path("token.json")):
    with path.open("wb") as f:
        f.write(orjson.dumps(token.to_dict()))


def load_token(path: Path = Path("token.json")) -> Optional[Token]:
    if path.exists():
        with path.open("rb") as f:
            data = orjson.loads(f.read())
            return Token.from_dict(data)
    return None


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def refresh_token(client_id: str, client_secret: str, token: Token) -> Token:
    """Refresh an expired token using the refresh token."""
    if not token.refresh_token:
        raise ValueError("No refresh token available")

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": token.refresh_token,
        "grant_type": "refresh_token",
    }

    response = httpx.post(
        "https://oauth2.googleapis.com/token", data=data, timeout=30.0
    )
    response.raise_for_status()

    new_token_data = response.json()

    # Ensure refresh token persists
    if not new_token_data.get("refresh_token"):
        new_token_data["refresh_token"] = token.refresh_token

    new_token = Token.from_dict(new_token_data)
    save_token(new_token)

    return new_token


def get_valid_token(config: dict, force_refresh: bool = False) -> Token:
    """Get a valid token, refreshing if necessary."""
    token = load_token()

    if not token:
        raise ValueError("No token found - please authenticate first")

    if force_refresh or token.is_expired():
        token = refresh_token(config["client_id"], config["client_secret"], token)

    return token


def get_video_details(video_ids: list[str], headers: dict) -> dict[str, dict]:
    video_details = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        params = {
            "part": "snippet",
            "id": ",".join(batch),
            "maxResults": 50,
        }
        url = f"{API_BASE_URL}/videos"
        response = make_request_with_retries("GET", url, headers, params=params)
        data = response.json()

        for item in data.get("items", []):
            video_details[item["id"]] = {
                "title": item["snippet"]["title"],
                "publishedAt": item["snippet"]["publishedAt"],
            }
    return video_details


def find_video_by_title(title: str, videos: dict[str, dict]) -> Optional[str]:
    if not title or not videos:
        return None

    titles_dict = {vid: details["title"] for vid, details in videos.items()}
    matches = process.extract(title, titles_dict.values(), scorer=fuzz.ratio, limit=3)

    if not matches:
        return None

    choices = [
        {"name": f"{title} (Match: {score}%)", "value": title, "style": "fg:green"}
        for title, score in matches
    ]
    choices.append({"name": "None of these matches", "value": None, "style": "fg:red"})

    selected = questionary.select(
        "Select the matching video:",
        choices=choices,
        style=questionary.Style(
            [
                ("qmark", "fg:yellow bold"),
                ("question", "fg:yellow bold"),
                ("pointer", "fg:cyan bold"),
                ("highlighted", "fg:cyan bold"),
                ("selected", "fg:green bold"),
            ]
        ),
    ).ask()

    if selected is None:
        return None

    for vid, vtitle in titles_dict.items():
        if vtitle == selected:
            return vid

    return None


def load_config() -> Config:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return Config(
        client_id=config.get("oauth", "client_id"),
        client_secret=config.get("oauth", "client_secret"),
        source_playlist_ids=[
            pid.strip()
            for pid in config.get("playlists", "source_playlist_ids").split(",")
        ],
        target_playlist_id=config.get("playlists", "target_playlist_id"),
    )


def save_token(token: Token):
    with open(TOKEN_FILE, "wb") as f:
        f.write(orjson.dumps(token.dict()))


def load_token() -> Optional[Token]:
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            data = orjson.loads(f.read())
            return Token(**data)
    return None


def get_auth_url(config: Config) -> str:
    params = {
        "client_id": config.client_id,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def authenticate(config: Config) -> Token:
    token = load_token()

    if token:
        console.print(
            f"[bold blue]Debug - Token found: Expires in {token.expiry_time - time.time():.0f} seconds[/bold blue]"
        )
        console.print(
            f"[bold blue]Debug - Has refresh token: {'Yes' if token.refresh_token else 'No'}[/bold blue]"
        )

    if token and not token.is_expired():
        return token

    console.print(
        "[bold yellow]No valid token found or token expired. Starting OAuth flow.[/bold yellow]"
    )
    auth_url = get_auth_url(config)
    console.print(
        f"Please open the following URL in your browser to authorize the application:\n[link]{auth_url}[/link]"
    )
    code = typer.prompt("After authorization, please enter the authorization code here")

    data = {
        "code": code,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "authorization_code",
    }

    response = make_request_with_retries("POST", TOKEN_URL, headers={}, data=data)
    token_data = response.json()
    token = Token.from_dict(token_data)
    save_token(token)
    console.print("[bold green]Authentication successful! Token saved.[/bold green]")
    return token


def refresh_token_if_needed(config: Config, token: Token) -> Token:
    if not token.is_expired():
        return token

    console.print("[bold blue]Debug - Token expired, attempting refresh[/bold blue]")

    if not token.refresh_token:
        console.print(
            "[bold red]No refresh token available. Please re-authenticate.[/bold red]"
        )
        return authenticate(config)

    data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "refresh_token": token.refresh_token,
        "grant_type": "refresh_token",
    }

    try:
        response = make_request_with_retries("POST", TOKEN_URL, headers={}, data=data)
        new_token_data = response.json()
        console.print("[bold blue]Debug - Refresh response:[/bold blue]")
        console.print(new_token_data)

        # Keep the existing refresh token as YouTube doesn't always return it
        new_token_data["refresh_token"] = token.refresh_token
        new_token = Token.from_dict(new_token_data)
        save_token(new_token)
        console.print("[bold green]Token refreshed successfully.[/bold green]")
        return new_token
    except Exception as e:
        console.print(f"[bold red]Debug - Refresh failed: {e!s}[/bold red]")
        return authenticate(config)


def get_headers(token: Token) -> dict:
    return {"Authorization": f"Bearer {token.access_token}"}


def log_api_call(method: str, url: str, status_code: int, response_time: float):
    logger.info(f"{method} {url} - Status: {status_code} - Time: {response_time:.2f}s")


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
def make_request_with_retries(
    method: str,
    url: str,
    headers: dict,
    params=None,
    json_payload=None,
    data=None,
):
    start_time = time.time()
    response = httpx.request(
        method,
        url,
        headers=headers,
        params=params,
        json=json_payload,
        data=data,
    )
    response_time = time.time() - start_time
    log_api_call(method, url, response.status_code, response_time)
    response.raise_for_status()
    return response


def load_video_cache() -> TinyDB:
    return TinyDB(CACHE_FILE)


def get_video_upload_date_from_cache(db: TinyDB, video_id: str) -> Optional[str]:
    Video = Query()
    result = db.table("video_cache").get(Video.id == video_id)
    if result:
        return result["publishedAt"]
    return None


def save_video_upload_date_to_cache(db: TinyDB, video_id: str, published_at: str):
    Video = Query()
    video_cache = db.table("video_cache")
    if not video_cache.contains(Video.id == video_id):
        video_cache.insert({"id": video_id, "publishedAt": published_at})


def get_playlist_videos(playlist_id: str, headers: dict) -> list[str]:
    videos = []
    next_page = None
    while True:
        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
        }
        if next_page:
            params["pageToken"] = next_page
        url = f"{API_BASE_URL}/playlistItems"

        response = make_request_with_retries("GET", url, headers, params=params)
        data = response.json()
        videos.extend(
            [item["contentDetails"]["videoId"] for item in data.get("items", [])]
        )
        next_page = data.get("nextPageToken")
        if not next_page:
            break
    return videos


def get_playlist_videos_with_item_ids(playlist_id: str, headers: dict) -> list[dict]:
    videos = []
    next_page = None
    while True:
        params = {
            "part": "contentDetails,id",
            "playlistId": playlist_id,
            "maxResults": 50,
        }
        if next_page:
            params["pageToken"] = next_page
        url = f"{API_BASE_URL}/playlistItems"
        response = make_request_with_retries("GET", url, headers, params=params)
        data = response.json()
        videos.extend(data.get("items", []))
        next_page = data.get("nextPageToken")
        if not next_page:
            break
    return videos


def get_video_published_date(video_id: str, headers: dict, db: TinyDB) -> Optional[str]:
    published_at = get_video_upload_date_from_cache(db, video_id)
    if published_at:
        return published_at
    params = {
        "part": "snippet",
        "id": video_id,
        "fields": "items(id,snippet(publishedAt))",
    }
    url = f"{API_BASE_URL}/videos"
    response = make_request_with_retries("GET", url, headers, params=params)
    data = response.json()
    if data.get("items"):
        item = data["items"][0]
        published_at = item["snippet"]["publishedAt"]
        save_video_upload_date_to_cache(db, video_id, published_at)
        return published_at
    console.print(f"[red]Video with ID {video_id} not found.[/red]")
    return None


def get_video_upload_dates(
    video_ids: list[str], headers: dict, db: TinyDB
) -> dict[str, str]:
    missing_ids = []
    upload_dates = {}

    for vid in video_ids:
        published_at = get_video_upload_date_from_cache(db, vid)
        if published_at:
            upload_dates[vid] = published_at
        else:
            missing_ids.append(vid)

    if not missing_ids:
        return upload_dates

    total_videos = len(missing_ids)
    batches = math.ceil(total_videos / 50)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("Fetching video upload dates...", total=total_videos)
        for i in range(batches):
            batch_ids = missing_ids[i * 50 : (i + 1) * 50]
            params = {
                "part": "snippet",
                "id": ",".join(batch_ids),
                "maxResults": 50,
                "fields": "items(id,snippet(publishedAt))",
            }
            url = f"{API_BASE_URL}/videos"
            response = make_request_with_retries("GET", url, headers, params=params)
            data = response.json()
            for item in data.get("items", []):
                vid = item["id"]
                published_at = item["snippet"]["publishedAt"]
                upload_dates[vid] = published_at
                save_video_upload_date_to_cache(db, vid, published_at)
            progress.update(task, advance=len(batch_ids))
    return upload_dates


def add_videos_to_playlist(
    playlist_id: str, video_ids: list[str], headers: dict, db: TinyDB
):
    existing_videos = get_playlist_videos(playlist_id, headers)

    existing_video_ids = set(existing_videos)

    new_videos = [vid for vid in video_ids if vid not in existing_video_ids]

    if not new_videos:
        console.print(
            "[bold yellow]No new videos to add. All videos are already in the target playlist.[/bold yellow]"
        )
        return

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("Adding videos...", total=len(new_videos))
        for video_id in new_videos:
            payload = {
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id,
                    },
                }
            }
            url = f"{API_BASE_URL}/playlistItems?part=snippet"
            make_request_with_retries("POST", url, headers, json_payload=payload)
            progress.update(task, advance=1)


def remove_videos_from_playlist(
    playlist_id: str, video_ids_to_remove: set, headers: dict
):
    existing_playlist_items = get_playlist_videos_with_item_ids(playlist_id, headers)
    video_id_to_playlist_item_id = {
        item["contentDetails"]["videoId"]: item["id"]
        for item in existing_playlist_items
    }

    playlist_item_ids_to_remove = [
        video_id_to_playlist_item_id[vid]
        for vid in video_ids_to_remove
        if vid in video_id_to_playlist_item_id
    ]

    if not playlist_item_ids_to_remove:
        console.print(
            "[bold yellow]No matching videos found to remove from the target playlist.[/bold yellow]"
        )
        return

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(
            "Removing videos...", total=len(playlist_item_ids_to_remove)
        )
        for playlist_item_id in playlist_item_ids_to_remove:
            url = f"{API_BASE_URL}/playlistItems"
            params = {"id": playlist_item_id}
            make_request_with_retries("DELETE", url, headers, params=params)
            progress.update(task, advance=1)


@app.command()
def combine_playlists():
    config = load_config()
    try:
        token = get_valid_token(config.model_dump())
    except ValueError:
        token = authenticate(config)
    headers = get_headers(token)
    db = load_video_cache()

    last_watched_title = questionary.text(
        "Enter the title of the last video you watched (leave blank if none)"
    ).ask()

    # Fetch video IDs from source playlists
    all_video_ids = []
    console.print("[bold blue]Fetching video IDs from source playlists...[/bold blue]")
    for pl_id in config.source_playlist_ids:
        videos = get_playlist_videos(pl_id, headers)
        if videos:
            all_video_ids.extend(videos)

    if not all_video_ids:
        console.print("[red]No videos found in playlists. Exiting.[/red]")
        return

    # Get video details including titles
    video_details = get_video_details(all_video_ids, headers)

    # Find last watched video using fuzzy search
    last_watched_video_id = None
    if last_watched_title:
        last_watched_video_id = find_video_by_title(last_watched_title, video_details)
        if last_watched_video_id:
            last_watched_published_at = video_details[last_watched_video_id][
                "publishedAt"
            ]
        else:
            console.print("[red]Could not find a matching video. Exiting.[/red]")
            return
    else:
        last_watched_published_at = None

    # Fetch video IDs and published dates from source playlists
    all_video_ids = []
    console.print("[bold blue]Fetching video IDs from source playlists...[/bold blue]")
    for pl_id in config.source_playlist_ids:
        console.print(f"Fetching videos from playlist: {pl_id}")
        videos = get_playlist_videos(pl_id, headers)
        if not videos:
            console.print(
                f"[yellow]No videos found in playlist {pl_id} or failed to fetch.[/yellow]"
            )
            continue
        all_video_ids.extend(videos)
        console.print(f"Fetched {len(videos)} videos from playlist {pl_id}")

    if not all_video_ids:
        console.print("[red]No new videos to process. Exiting.[/red]")
        return

    # Get upload dates for all videos
    upload_dates = get_video_upload_dates(all_video_ids, headers, db)

    if not upload_dates:
        console.print(
            "[red]No valid videos with upload dates to process. Exiting.[/red]"
        )
        return

    # Exclude videos published before the last watched video's published date
    if last_watched_published_at:
        videos_to_consider = {
            vid: date
            for vid, date in upload_dates.items()
            if date > last_watched_published_at
        }
    else:
        videos_to_consider = upload_dates

    if not videos_to_consider:
        console.print(
            "[yellow]No new videos to add after filtering by last watched video. Exiting.[/yellow]"
        )
        return

    # Get existing videos in target playlist
    console.print(
        "[bold blue]Fetching existing videos from target playlist...[/bold blue]"
    )
    existing_playlist_items = get_playlist_videos_with_item_ids(
        config.target_playlist_id, headers
    )

    existing_video_ids = {
        item["contentDetails"]["videoId"] for item in existing_playlist_items
    }

    # Map video IDs to playlist item IDs
    video_id_to_playlist_item_id = {
        item["contentDetails"]["videoId"]: item["id"]
        for item in existing_playlist_items
    }

    # Determine which videos need to be added
    videos_to_add = set(videos_to_consider.keys()) - existing_video_ids

    # Determine which videos need to be removed
    videos_to_remove = existing_video_ids - set(videos_to_consider.keys())

    # Add new videos
    if videos_to_add:
        # Sort videos to add by published date

        sorted_videos_to_add = sorted(
            [(vid, videos_to_consider[vid]) for vid in videos_to_add],
            key=lambda x: x[1],
        )
        sorted_video_ids_to_add = [vid for vid, date in sorted_videos_to_add]

        console.print(
            f"[bold blue]Adding {len(sorted_video_ids_to_add)} new videos to the target playlist...[/bold blue]"
        )
        add_videos_to_playlist(
            config.target_playlist_id, sorted_video_ids_to_add, headers, db
        )
    else:
        console.print("[yellow]No new videos to add.[/yellow]")

    # Remove videos

    if videos_to_remove:
        console.print(
            f"[bold blue]Removing {len(videos_to_remove)} videos from the target playlist...[/bold blue]"
        )
        remove_videos_from_playlist(
            config.target_playlist_id, videos_to_remove, headers
        )
    else:
        console.print("[yellow]No videos to remove.[/yellow]")

    console.print("[bold green]Playlist synchronization complete.[/bold green]")


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="WARNING")
    logger.add("yt_playlist_creator.log", level="WARNING", rotation="10 MB")
    app()
