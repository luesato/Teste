"""LLM-driven capture: for pages you can't reach by URL alone.

Use this only when getting to the view requires reasoning ("open Reports,
switch the range to last 30 days, screenshot the revenue chart"). If you can
name the URL, use shoot.py instead - it is free, faster and deterministic.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from browser_use import Agent, BrowserProfile, BrowserSession

import chrome_paths


def build_llm(name: str):
    """Pick a chat model. Each needs its own key in .env - see README."""
    if name.startswith("claude"):
        from browser_use import ChatAnthropic

        if not os.getenv("ANTHROPIC_API_KEY"):
            raise SystemExit(
                "ANTHROPIC_API_KEY is not set.\n"
                "Note: this must be an Anthropic API key from console.anthropic.com.\n"
                "A Claude.ai subscription login does not work here."
            )
        return ChatAnthropic(model=name, temperature=0.0)

    if name.startswith("gpt"):
        from browser_use import ChatOpenAI

        return ChatOpenAI(model=name, temperature=0.0)

    if name.startswith("gemini"):
        from browser_use import ChatGoogle

        return ChatGoogle(model=name, temperature=0.0)

    # Anything else is treated as a local Ollama tag, e.g. "qwen2.5vl:7b".
    from browser_use import ChatOllama

    return ChatOllama(model=name)


async def run(args: argparse.Namespace) -> int:
    load_dotenv()

    out_dir = Path(args.out) / dt.date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)

    user_data_dir = Path(args.user_data_dir) if args.user_data_dir else chrome_paths.find_user_data_dir()
    executable = Path(args.executable) if args.executable else chrome_paths.find_executable()
    if not user_data_dir or not executable:
        print("Could not locate Chrome. Run: python check_setup.py", file=sys.stderr)
        return 2

    profile = BrowserProfile(
        user_data_dir=str(user_data_dir),
        profile_directory=args.profile,
        executable_path=str(executable),
        headless=False,
        # Hard boundary: the agent cannot navigate outside these hosts even if
        # a page tries to talk it into doing so.
        allowed_domains=args.allow,
        chromium_sandbox=not args.no_sandbox,
        args=["--no-sandbox", "--disable-dev-shm-usage"] if args.no_sandbox else [],
    )
    session = BrowserSession(browser_profile=profile)

    agent = Agent(
        task=args.task,
        llm=build_llm(args.model),
        browser_session=session,
        use_vision=True,
    )

    await session.start()
    try:
        await agent.run(max_steps=args.max_steps)
        dest = out_dir / f"{args.name}.png"
        await session.take_screenshot(path=str(dest.resolve()), full_page=True)
        print(f"saved {dest}")
    finally:
        await session.stop()
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="LLM-driven screenshot of a logged-in app.")
    p.add_argument("task", help="What to do before the screenshot, in plain English")
    p.add_argument("--name", default="capture", help="Output filename stem")
    p.add_argument("--allow", nargs="+", required=True, help="Hostnames the agent may visit")
    p.add_argument("--model", default="claude-sonnet-4-0")
    p.add_argument("--out", default="shots")
    p.add_argument("--profile", default="Default")
    p.add_argument("--user-data-dir", default=None)
    p.add_argument("--executable", default=None)
    p.add_argument("--max-steps", type=int, default=25, help="Hard cap so a loop cannot burn your budget")
    p.add_argument("--no-sandbox", action="store_true")
    return asyncio.run(run(p.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
