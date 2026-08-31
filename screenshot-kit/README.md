# Screenshot kit for logged-in apps

Capture screenshots of web apps you are already signed into, on your own machine,
using your real Chrome profile. Built and tested against **browser-use 0.13.8**.

Two scripts, and the choice between them matters:

| | `shoot.py` | `agent_shot.py` |
|---|---|---|
| Needs an API key | No | Yes |
| Cost per run | Zero | Tokens per step |
| Reliability | Deterministic | Varies |
| Use when | You know the URLs | Reaching the view needs reasoning |

**Start with `shoot.py`.** Most "screenshot my dashboards" jobs are a fixed URL
list, and an LLM adds cost and failure modes without adding capability.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python check_setup.py             # finds Chrome + lists your profiles
```

`check_setup.py` prints the profile folder names (`Default`, `Profile 1`, ...)
next to the account each one belongs to. You need the folder name.

```bash
cp targets.example.yaml targets.yaml   # then edit
python shoot.py --profile "Profile 1"
```

Output lands in `shots/YYYY-MM-DD/<name>.png`.

---

## How logins actually work here — read this before debugging

browser-use **copies your Chrome profile to a temp directory on every run** and
drives the copy. This is in `browser/profile.py::_copy_profile`, and it has three
consequences that will otherwise waste your afternoon:

1. **Close Chrome before running.** The copy fails on locked files while Chrome
   holds the profile. The error names this explicitly.
2. **Log in using normal Chrome, not the agent's browser.** Cookies flow one way:
   your real profile is copied *in*. Anything the agent does — a fresh login, a
   refreshed token — is thrown away when the temp directory is deleted.
3. **Your real profile is never modified.** The agent cannot corrupt or log out
   your actual browser. That is a genuine safety property, not just a limitation.

So the working loop is: sign in normally in Chrome once → close Chrome → run the
script. Re-authenticate in Chrome whenever a session expires.

### If you cannot close Chrome

Attach to a running instance instead. No copying, live session, and it persists —
but the agent is now inside your real browser, so treat it as supervised:

```bash
# start Chrome yourself with a debugging port
chrome --remote-debugging-port=9222

python shoot.py --cdp http://127.0.0.1:9222
```

---

## Security — the part that matters

You are handing an automated process your live session cookies. That bypasses
passwords and 2FA, because it is already inside.

- **Use a dedicated Chrome profile.** Make a second Chrome profile (Chrome menu →
  your avatar → Add), sign it into only the apps you are capturing, and point
  `--profile` at that. This is the single highest-value step.
- **Never point this at a profile holding your primary email.** Email is the root
  of every password reset you own.
- **`shoot.py` restricts the browser** to exactly the hostnames in `targets.yaml`
  via `allowed_domains`. `agent_shot.py` requires `--allow` for the same reason —
  an LLM that reads a hostile page cannot be talked into navigating off-list.
- **Never put passwords in this repo.** Nothing here asks for credentials, and
  `.gitignore` excludes `.env`, `shots/`, and `targets.yaml` (your URLs can be
  sensitive on their own).

`agent_shot.py` is the higher-risk script: the model reads page content, and page
content can contain instructions aimed at it. `--max-steps` caps the damage a loop
can do to your bill; `--allow` caps where it can go.

---

## Which model

`shoot.py` needs none. For `agent_shot.py`:

```bash
python agent_shot.py "open Reports and set the range to last 30 days" \
  --allow app.example.com --name reports --model claude-sonnet-4-0
```

- `--model claude-*` → needs `ANTHROPIC_API_KEY` from **console.anthropic.com**.
  A Claude.ai / Claude Code subscription login does **not** work for this — the
  library calls the API directly and needs a metered key.
- `--model gpt-*` → `OPENAI_API_KEY`; `--model gemini-*` → `GOOGLE_API_KEY`.
- Anything else is treated as a local **Ollama** tag (`--model qwen2.5vl:7b`) and
  costs nothing. Be realistic: small local models are weak at deciding where to
  click from a screenshot. Fine for simple flows, unreliable for dense dashboards.

---

## Scheduling it

Once `shoot.py` works by hand:

- **Linux/macOS** — `crontab -e`:
  `0 7 * * 1-5 cd /path/to/screenshot-kit && .venv/bin/python shoot.py --profile "Profile 1"`
- **Windows** — Task Scheduler, action `.venv\Scripts\python.exe shoot.py`, start-in
  set to this folder.

Headless (`--headless`) is off by default on purpose: some apps render or behave
differently without a visible window, and you want to *see* the first few runs.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `Unable to copy Chrome profile ... locked` | Chrome is open. Close it, or use `--cdp`. |
| Screenshot shows a login page | That profile is not signed in, or the session expired. Sign in via Chrome, close it, rerun. `shoot.py` warns when it detects this. |
| Hangs at launch in Docker/WSL | Add `--no-sandbox`. |
| Blank or half-rendered charts | Raise `settle` for that target in `targets.yaml`. |
