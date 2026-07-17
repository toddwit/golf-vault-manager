from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_FILE = PROJECT_ROOT / "settings.json"

DEFAULT_SETTINGS = {
    "vault_path": r"C:\.Personal\Golf Vault"
}


def load_settings() -> dict:
    """Load application settings, creating defaults if necessary."""

    if not SETTINGS_FILE.exists():
        with SETTINGS_FILE.open("w", encoding="utf-8") as file:
            json.dump(DEFAULT_SETTINGS, file, indent=4)

        return DEFAULT_SETTINGS.copy()

    with SETTINGS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


settings = load_settings()

VAULT_PATH = Path(
    settings.get(
        "vault_path",
        DEFAULT_SETTINGS["vault_path"],
    )
)

DEFAULT_TOPICS = [
    "Grip",
    "Setup",
    "Backswing",
    "Transition",
    "Clubface Control",
    "Driver",
    "Iron Play",
    "Chipping",
    "Bunker Play",
    "Putting",
]

MIN_RATING = 1
MAX_RATING = 5
DEFAULT_RATING = 3