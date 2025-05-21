from openapi_client.models.authenticate_user_by_name import AuthenticateUserByName
from openapi_client.api.user_api import UserApi
from openapi_client.api.user_views_api import UserViewsApi
from openapi_client.api.items_api import ItemsApi
from openapi_client.configuration import Configuration
from openapi_client.api_client import ApiClient
from rich import print
from iterfzf import iterfzf

from loguru import logger
import json
import os
from pathlib import Path
import questionary
from addict import Dict

# Default URL if none provided by user
DEFAULT_URL = "http://localhost:8096"

# Use XDG_CONFIG_HOME or fallback to ~/.config
CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "jelly"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> Dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Dict(data)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
    return Dict()


def save_config(config: Dict):
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save config: {e}")


def prompt_server_url() -> str:
    url = questionary.text("Server URL:", default=DEFAULT_URL).ask()
    return url.strip() if url else DEFAULT_URL


def prompt_credentials():
    username = questionary.text("Username:").ask()
    password = questionary.password("Password:").ask()
    return username, password


config_data = load_config()

if not config_data.server_url or not config_data.server_url.strip():
    config_data.server_url = prompt_server_url()
    save_config(config_data)

# Update Configuration and ApiClient with server_url from config
config = Configuration(host=config_data.server_url)
api_client = ApiClient(config)
user_api = UserApi(api_client)
user_views_api = UserViewsApi(api_client)
items_api = ItemsApi(api_client)

# Prepare authorization header template (without token)
authorization_template = 'MediaBrowser , Client="other", Device="script", DeviceId="script", Version="0.0.0", Token="{}"'


def get_headers(token: str) -> dict:
    return {"Authorization": authorization_template.format(token)}


def authenticate(username: str, password: str):
    auth_request = AuthenticateUserByName(
        username=username,
        pw=password,
    )

    try:
        auth_result = user_api.authenticate_user_by_name(
            auth_request,
            _headers=get_headers(""),  # initial blank token
        )
        return auth_result
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        return None


def authenticate_and_save():
    username, password = prompt_credentials()
    auth_result = authenticate(username, password)
    if auth_result and getattr(auth_result, "access_token", None):
        config_data.access_token = auth_result.access_token
        config_data.user_id = auth_result.user.id
        save_config(config_data)
        return auth_result.access_token, auth_result.user.id
    else:
        logger.error("Authentication failed or no access token received.")
        return None


def get_user_views(user_id: str):
    views = user_views_api.get_user_views(user_id=user_id, _headers=headers)
    view_info = [{k: v for (k, v) in view} for view in views.items]
    return view_info


def get_items(parent_id: str):
    items = items_api.get_items(parent_id=parent_id, _headers=headers)
    item_info = [{k: v for (k, v) in view} for view in items.items]
    for item in item_info:
        if item["type"] == "Episode":
            item["name"] = f"Episode {item['index_number']} - {item['name']}"
    try:
        sorted_list = sorted(item_info, key=lambda d: d["index_number"], reverse=True)
    except (TypeError, KeyError):
        sorted_list = sorted(item_info, key=lambda d: d["name"], reverse=True)

    return sorted_list


def fzf_select(list_of_dicts: list[dict], location_list: list[dict]) -> dict:
    item_choices = [choice["name"] for choice in list_of_dicts]
    user_choice = iterfzf(item_choices)
    user_choice = [
        dictionary for dictionary in list_of_dicts if dictionary["name"] == user_choice
    ][0]

    new_location = add_to_location(
        {"name": user_choice["name"], "id": user_choice["id"]},
        location_list,
    )
    return user_choice, new_location


def add_to_location(choice_location: dict, location_list: list[dict]) -> list[dict]:
    location_string = f"{location_list['location_string']}/{choice_location['name']}"
    location_id = f"{location_list['location_id']}/{choice_location['id']}"
    return {"location_string": location_string, "location_id": location_id}


if __name__ == "__main__":
    token = config_data.get("access_token")
    user_id = config_data.get("user_id")
    if not token:
        token, user_id = authenticate_and_save()
    if not token:
        print("[red]Authentication failed.[/red]")
        exit(1)

    headers = get_headers(token)

    location = {"location_string": "", "location_id": ""}

    # Example test call to verify token works
    choice, location = fzf_select(get_user_views(user_id), location)
    next_choice = get_items(choice["id"])
    choice, location = fzf_select(next_choice, location)
    next_choice = get_items(choice["id"])
    choice, location = fzf_select(next_choice, location)
    next_choice = get_items(choice["id"])
    choice, location = fzf_select(next_choice, location)
    next_choice = get_items(choice["id"])
    print(choice, location)
