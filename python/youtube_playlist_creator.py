import configparser
import json
import math
import time
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlencode

import httpx
import typer
from loguru import logger
from pydantic import BaseModel
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn

app = typer.Typer()
console = Console()

# Configuration and Token Files
CONFIG_FILE = Path("yt_playlist_creator.ini")
TOKEN_FILE = Path("yt_playlist_creator.json")
CACHE_FILE = Path("yt_playlist_cache.json")

# OAuth and API Endpoints
SCOPES = ["https://www.googleapis.com/auth/youtube"]
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
API_BASE_URL = "https://www.googleapis.com/youtube/v3"


class Config(BaseModel):
    client_id: str
    client_secret: str
    source_playlist_ids: List[str]
    target_playlist_id: str
    watched_playlist_ids: List[str]


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
        watched_playlist_ids=[
            pid.strip()
            for pid in config.get(
                "playlists", "watched_playlist_ids", fallback="WL,LL"
            ).split(",")
        ],
    )


def save_token(token: dict):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token, f)


def load_token() -> dict:
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return {}


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


def authenticate(config: Config) -> dict:
    token = load_token()
    if token:
        return token

    console.print(
        "[bold yellow]No valid token found. Starting OAuth flow.[/bold yellow]"
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

    try:
        response = make_request_with_retries("POST", TOKEN_URL, headers={}, data=data)
        token = response.json()
        save_token(token)
        console.print(
            "[bold green]Authentication successful! Token saved.[/bold green]"
        )
        return token
    except Exception as e:
        console.print(f"[red]Authentication failed: {e!s}[/red]")
        raise


def refresh_token_if_needed(config: Config, token: dict) -> dict:
    if token.get("expires_in", 0) < 60:
        data = {
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "refresh_token": token.get("refresh_token"),
            "grant_type": "refresh_token",
        }
        try:
            response = make_request_with_retries(
                "POST", TOKEN_URL, headers={}, data=data
            )
            new_token = response.json()
            token.update(new_token)
            save_token(token)
            console.print("[bold green]Token refreshed successfully.[/bold green]")
        except Exception as e:
            console.print(f"[red]Token refresh failed: {e!s}[/red]")
            raise
    return token


def get_headers(token: dict) -> dict:
    return {"Authorization": f"Bearer {token['access_token']}"}


def log_api_call(method: str, url: str, status_code: int, response_time: float):
    logger.info(f"{method} {url} - Status: {status_code} - Time: {response_time:.2f}s")


def make_request_with_retries(
    method: str,
    url: str,
    headers: dict,
    params=None,
    json_payload=None,
    data=None,
    max_retries=5,
):
    for attempt in range(1, max_retries + 1):
        try:
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
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [429, 500, 502, 503, 504]:
                wait_time = 2**attempt
                console.print(
                    f"[yellow]API rate limit reached or server error ({e.response.status_code}). "
                    f"Retrying in {wait_time} seconds...[/yellow]"
                )
                time.sleep(wait_time)
            else:
                console.print(
                    f"[red]HTTP error: {e.response.status_code} - {e.response.text}[/red]"
                )
                raise
        except Exception as e:
            console.print(f"[red]Unexpected error: {e!s}[/red]")
            raise
    console.print("[red]Max retries exceeded. Exiting.[/red]")
    raise Exception("Max retries exceeded.")


def load_video_cache() -> Dict[str, str]:
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_video_cache(cache: Dict[str, str]):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def get_playlist_videos(playlist_id: str, headers: dict) -> List[str]:
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
        try:
            response = make_request_with_retries("GET", url, headers, params=params)
            data = response.json()
            videos.extend(
                [item["contentDetails"]["videoId"] for item in data.get("items", [])]
            )
            next_page = data.get("nextPageToken")
            if not next_page:
                break
        except Exception as e:
            console.print(
                f"[red]Failed to fetch videos from playlist {playlist_id}: {e!s}[/red]"
            )
            break
    return videos


def get_video_upload_dates(
    video_ids: List[str], headers: dict, cache: Dict[str, str]
) -> Dict[str, str]:
    missing_ids = [vid for vid in video_ids if vid not in cache]
    if not missing_ids:
        return {vid: cache[vid] for vid in video_ids}

    upload_dates = {}
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
            try:
                response = make_request_with_retries("GET", url, headers, params=params)
                data = response.json()
                for item in data.get("items", []):
                    vid = item["id"]
                    published_at = item["snippet"]["publishedAt"]
                    upload_dates[vid] = published_at
                    cache[vid] = published_at  # Update cache
                progress.update(task, advance=len(batch_ids))
            except Exception as e:
                console.print(f"[red]Error fetching upload dates: {e!s}[/red]")
                raise
    save_video_cache(cache)
    return {vid: upload_dates[vid] for vid in video_ids if vid in upload_dates}


def get_watched_videos(watched_playlist_ids: List[str], headers: dict) -> set:
    watched_videos = set()
    for pl_id in watched_playlist_ids:
        next_page = None
        while True:
            params = {
                "part": "contentDetails",
                "playlistId": pl_id,
                "maxResults": 50,
            }
            if next_page:
                params["pageToken"] = next_page
            url = f"{API_BASE_URL}/playlistItems"
            try:
                response = make_request_with_retries("GET", url, headers, params=params)
                data = response.json()
                watched_videos.update(
                    [
                        item["contentDetails"]["videoId"]
                        for item in data.get("items", [])
                    ]
                )
                next_page = data.get("nextPageToken")
                if not next_page:
                    break
            except Exception as e:
                console.print(
                    f"[red]Failed to fetch videos from watched playlist {pl_id}: {e!s}[/red]"
                )
                break
    return watched_videos


def get_existing_videos(playlist_id: str, headers: dict) -> set:
    existing_videos = set()
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
        try:
            response = make_request_with_retries("GET", url, headers, params=params)
            data = response.json()
            existing_videos.update(
                item["contentDetails"]["videoId"] for item in data.get("items", [])
            )
            next_page = data.get("nextPageToken")
            if not next_page:
                break
        except Exception as e:
            console.print(
                f"[red]Failed to fetch existing videos from target playlist {playlist_id}: {e!s}[/red]"
            )
            break
    return existing_videos


def add_videos_to_playlist(playlist_id: str, video_ids: List[str], headers: dict):
    """Add a list of video IDs to the target playlist."""
    existing_videos = get_existing_videos(playlist_id, headers)
    new_videos = [vid for vid in video_ids if vid not in existing_videos]

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
            try:
                # Include 'part=snippet' as a query parameter
                url = f"{API_BASE_URL}/playlistItems?part=snippet"
                response = make_request_with_retries(
                    "POST", url, headers, json_payload=payload
                )
                progress.update(task, advance=1)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    console.print(
                        f"[red]Failed to add video ID {video_id}: Access Forbidden[/red]"
                    )
                else:
                    console.print(
                        f"[red]Failed to add video ID {video_id}: {e.response.status_code} - {e.response.text}[/red]"
                    )
            except Exception as e:
                console.print(
                    f"[red]An unexpected error occurred while adding video ID {video_id}: {e!s}[/red]"
                )


@app.command()
def combine_playlists():
    """Combine videos from multiple public source playlists into a target playlist,
    excluding videos you've already watched, and sort them by upload date.
    """
    config = load_config()
    token = authenticate(config)
    token = refresh_token_if_needed(config, token)
    headers = get_headers(token)

    # Load video cache
    video_cache = load_video_cache()

    # Fetch watched videos
    console.print(
        "[bold blue]Fetching watched videos from watched playlists...[/bold blue]"
    )
    watched_videos = get_watched_videos(config.watched_playlist_ids, headers)
    console.print(
        f"[bold blue]Total watched videos fetched: {len(watched_videos)}[/bold blue]"
    )

    # Fetch videos from source playlists
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
        # Exclude watched videos immediately
        new_videos = [vid for vid in videos if vid not in watched_videos]
        all_video_ids.extend(new_videos)
        console.print(f"Fetched {len(new_videos)} new videos from playlist {pl_id}")

    if not all_video_ids:
        console.print(
            "[red]No new videos to process after excluding watched videos. Exiting.[/red]"
        )
        return

    # Remove duplicates
    unique_video_ids = list(dict.fromkeys(all_video_ids))
    console.print(
        f"[bold blue]Total unique videos fetched: {len(unique_video_ids)}[/bold blue]"
    )

    # Fetch upload dates
    console.print("[bold blue]Fetching upload dates for all videos...[/bold blue]")
    upload_dates = get_video_upload_dates(unique_video_ids, headers, video_cache)

    # Filter out videos without upload dates (e.g., private or deleted videos)
    filtered_videos = {
        vid: date for vid, date in upload_dates.items() if vid in unique_video_ids
    }
    console.print(
        f"[bold blue]Total videos with valid upload dates: {len(filtered_videos)}[/bold blue]"
    )

    if not filtered_videos:
        console.print("[red]No valid videos with upload dates to add. Exiting.[/red]")
        return

    # Sort videos by upload date (oldest first)
    sorted_videos = sorted(filtered_videos.items(), key=lambda item: item[1])

    # Extract sorted video IDs
    sorted_video_ids = [vid for vid, date in sorted_videos]

    console.print(
        "[bold blue]Adding sorted videos to the target playlist...[/bold blue]"
    )
    add_videos_to_playlist(config.target_playlist_id, sorted_video_ids, headers)
    console.print(
        "[bold green]All new videos have been added to the target playlist.[/bold green]"
    )


if __name__ == "__main__":
    # Configure logging
    logger.add("yt_playlist_creator.log", rotation="10 MB")
    app()
