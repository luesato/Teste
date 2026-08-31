"""Screenshot a fixed list of URLs using your existing Chrome logins.

No LLM, no API key, no per-run cost. Use this whenever you already know the URLs.
Use agent_shot.py only when reaching the page needs reasoning.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml
from browser_use import BrowserProfile, BrowserSession

import chrome_paths


def load_targets(path: Path) -> tuple[list[dict], dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    defaults = data.get("defaults") or {}
    targets = data.get("targets") or []
    if not targets:
        raise SystemExit(f"No targets defined in {path}")
    return targets, defaults


def allowed_domains(targets: list[dict]) -> list[str]:
    """Restrict the browser to exactly the hosts we intend to visit."""
    hosts = set()
    for t in targets:
        host = urlparse(t["url"]).hostname
        if host:
            hosts.add(host)
    return sorted(hosts)


async def capture(args: argparse.Namespace) -> int:
    targets, defaults = load_targets(Path(args.targets))

    out_dir = Path(args.out) / dt.date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.cdp:
        # Attach to a Chrome you started yourself with --remote-debugging-port.
        # Uses the live session; nothing is copied.
        session = BrowserSession(cdp_url=args.cdp)
        print(f"Attaching to running Chrome at {args.cdp}")
    else:
        user_data_dir = Path(args.user_data_dir) if args.user_data_dir else chrome_paths.find_user_data_dir()
        executable = Path(args.executable) if args.executable else chrome_paths.find_executable()

        if not user_data_dir or not executable:
            print("Could not locate Chrome. Run: python check_setup.py", file=sys.stderr)
            return 2

        print(f"Chrome:       {executable}")
        print(f"User data:    {user_data_dir}")
        print(f"Profile:      {args.profile}")
        print(
            "\nbrowser-use copies this profile to a temp directory and drives the copy.\n"
            "Your real profile is never written to - but Chrome must be CLOSED,\n"
            "or the copy fails on locked files.\n"
        )

        profile = BrowserProfile(
            user_data_dir=str(user_data_dir),
            profile_directory=args.profile,
            executable_path=str(executable),
            headless=args.headless,
            allowed_domains=allowed_domains(targets),
            window_size={"width": args.width, "height": args.height},
            chromium_sandbox=not args.no_sandbox,
            args=["--no-sandbox", "--disable-dev-shm-usage"] if args.no_sandbox else [],
        )
        session = BrowserSession(browser_profile=profile)

    await session.start()
    failures = 0
    try:
        for target in targets:
            name = target["name"]
            url = target["url"]
            settle = target.get("settle", defaults.get("settle", 4))
            full_page = target.get("full_page", defaults.get("full_page", True))
            dest = out_dir / f"{name}.png"

            try:
                print(f"  -> {name}: {url}")
                await session.navigate_to(url)
                await asyncio.sleep(settle)
                await session.take_screenshot(path=str(dest.resolve()), full_page=full_page)
                landed = await session.get_current_page_url()
                if _looks_like_login(landed):
                    print(f"     ! redirected to {landed} - that profile is not logged in")
                    failures += 1
                else:
                    print(f"     saved {dest}")
            except Exception as exc:
                print(f"     ! failed: {exc}")
                failures += 1
    finally:
        await session.stop()

    print(f"\nDone. {len(targets) - failures}/{len(targets)} captured into {out_dir}")
    return 1 if failures else 0


def _looks_like_login(url: str) -> bool:
    lowered = (url or "").lower()
    return any(hint in lowered for hint in ("/login", "/signin", "accounts.google.com", "/auth/"))


def main() -> int:
    p = argparse.ArgumentParser(description="Screenshot logged-in pages with your Chrome profile.")
    p.add_argument("--targets", default="targets.yaml")
    p.add_argument("--out", default="shots")
    p.add_argument("--profile", default="Default", help="Chrome profile folder, e.g. 'Profile 1'")
    p.add_argument("--user-data-dir", default=None)
    p.add_argument("--executable", default=None)
    p.add_argument("--cdp", default=None, help="Attach to running Chrome, e.g. http://127.0.0.1:9222")
    p.add_argument("--headless", action="store_true", help="Off by default: many sites behave differently headless")
    p.add_argument("--no-sandbox", action="store_true", help="Needed inside Docker/WSL; leave off on a normal desktop")
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    return asyncio.run(capture(p.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
