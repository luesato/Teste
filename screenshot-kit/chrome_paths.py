"""Locate the local Chrome binary and profile directory across platforms."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Chrome's own naming: the folder passed to --user-data-dir holds one or more
# profiles ("Default", "Profile 1", ...). You need both to target a specific login.

_USER_DATA_DIRS = {
    "win32": [r"%LOCALAPPDATA%\Google\Chrome\User Data"],
    "darwin": ["~/Library/Application Support/Google/Chrome"],
    "linux": ["~/.config/google-chrome", "~/.config/chromium"],
}

_EXECUTABLES = {
    "win32": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ],
    "darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
    "linux": ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium"],
}


def _platform() -> str:
    if sys.platform.startswith("win"):
        return "win32"
    if sys.platform == "darwin":
        return "darwin"
    return "linux"


def _expand(raw: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(raw)))


def find_user_data_dir() -> Path | None:
    for raw in _USER_DATA_DIRS[_platform()]:
        path = _expand(raw)
        if path.is_dir():
            return path
    return None


def find_executable() -> Path | None:
    for raw in _EXECUTABLES[_platform()]:
        path = _expand(raw)
        if path.exists():
            return path
    return None


def list_profiles(user_data_dir: Path) -> list[str]:
    """Return the profile folder names inside a Chrome user-data directory."""
    if not user_data_dir.is_dir():
        return []
    names = []
    for child in sorted(user_data_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name == "Default" or child.name.startswith("Profile "):
            names.append(child.name)
    return names


def profile_label(user_data_dir: Path, profile_directory: str) -> str:
    """Read the human-facing profile name Chrome shows in its profile switcher."""
    import json

    local_state = user_data_dir / "Local State"
    if not local_state.exists():
        return profile_directory
    try:
        data = json.loads(local_state.read_text(encoding="utf-8"))
        info = data["profile"]["info_cache"][profile_directory]
        name = info.get("name") or profile_directory
        email = info.get("user_name") or ""
        return f"{name} <{email}>" if email else name
    except Exception:
        return profile_directory
