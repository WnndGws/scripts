from openapi_client.models.authenticate_user_by_name import AuthenticateUserByName
from openapi_client.api.user_api import UserApi
from openapi_client.configuration import Configuration
from openapi_client.api_client import ApiClient
from rich import print

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


if __name__ == "__main__":
    token = config_data.get("access_token")
    user_id = config_data.get("user_id")
    if not token:
        token, user_id = authenticate_and_save()
    if not token:
        print("[red]Authentication failed.[/red]")
        exit(1)

    headers = get_headers(token)

    # Example test call to verify token works
    try:
        test_result = user_api.get_current_user(_headers=headers)
        print(test_result)
    except Exception as e:
        logger.error(f"API call failed: {e}")
        print("[red]API call failed. Possibly invalid token.[/red]")
        exit(1)
