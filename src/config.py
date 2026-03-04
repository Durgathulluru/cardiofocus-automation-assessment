import os
from dataclasses import dataclass

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

@dataclass
class UiConfig:
    base_url: str
    username: str
    password: str
    device_id: str
    expected_status: str
    headless: bool

@dataclass
class ApiConfig:
    base_url: str
    device_id: str
    expected_status: str
    auth_mode: str          # token | basic
    token: str
    basic_user: str
    basic_pass: str

def load_ui_config() -> UiConfig:
    return UiConfig(
        base_url=env("UI_BASE_URL", "https://portal.cardiofocus.com"),
        username=env("UI_USERNAME"),
        password=env("UI_PASSWORD"),
        device_id=env("DEVICE_ID", "ABC123"),
        expected_status=env("EXPECTED_STATUS", "OK"),
        headless=env("HEADLESS", "true").lower() == "true",
    )

def load_api_config() -> ApiConfig:
    return ApiConfig(
        base_url=env("API_BASE_URL", "https://portal.cardiofocus.com"),
        device_id=env("DEVICE_ID", "ABC123"),
        expected_status=env("EXPECTED_STATUS", "OK"),
        auth_mode=env("API_AUTH_MODE", "token").lower(),
        token=env("API_TOKEN"),
        basic_user=env("API_BASIC_USER"),
        basic_pass=env("API_BASIC_PASS"),
    )