"""Verify the local setup before running a capture. Reads nothing sensitive."""

from __future__ import annotations

import sys

import chrome_paths


def main() -> int:
    print("browser-use screenshot kit - setup check\n")
    ok = True

    try:
        import browser_use  # noqa: F401

        from importlib.metadata import version

        print(f"  [ok]   browser-use {version('browser-use')}")
    except Exception as exc:
        print(f"  [FAIL] browser-use not importable: {exc}")
        print("         run: pip install -r requirements.txt")
        ok = False

    exe = chrome_paths.find_executable()
    if exe:
        print(f"  [ok]   Chrome binary: {exe}")
    else:
        print("  [FAIL] Chrome not found. Pass --executable /path/to/chrome")
        ok = False

    udd = chrome_paths.find_user_data_dir()
    if not udd:
        print("  [FAIL] Chrome user-data dir not found. Pass --user-data-dir")
        return 1

    print(f"  [ok]   User data dir: {udd}")

    profiles = chrome_paths.list_profiles(udd)
    if not profiles:
        print("  [FAIL] No profiles found inside that directory.")
        return 1

    print("\n  Profiles available (use the folder name with --profile):\n")
    for name in profiles:
        label = chrome_paths.profile_label(udd, name)
        print(f"    {name:<12} {label}")

    print(
        "\n  Reminder: pick a profile that is logged into ONLY what the capture needs.\n"
        "  Do not point this at a profile holding your primary email or banking."
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
