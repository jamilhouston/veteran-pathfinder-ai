# Veteran Pathfinder — Career Transition Assistant

**Applied AI · Workforce transition · Responsible product design**

[Try the Replit demo](https://pathfinder-replitzip.replit.app) · [Portfolio and other projects](https://jamilhouston.com/labs)

## Portfolio case study

Pathfinder is an exploratory career-planning web application built around a specific problem: helping veterans translate military responsibilities into language and possibilities that make sense in civilian employment. Its goal is to **support user judgment**, not select careers on a veteran's behalf.

**My contribution:** identified the veteran transition use case, defined the desired experience and privacy priorities, built and iterated the application using Replit/AI-assisted development, and documented the architecture and project presentation.

**Stack:** Python, Flask, Waitress, server-rendered HTML/Jinja, CSS, JavaScript, optional OpenAI Responses API, and automated Python unit tests.

**What the demo offers:** a guest profile workflow; illustrative, keyword-ranked career paths; transferable-skills explanations; gaps and next steps; resume draft text; export/delete controls; and a separately consented optional AI generation mode.

**Verification:** ten automated backend tests passed in an October 2026 source inspection. Real-provider AI success and professional counselor evaluation were not independently confirmed.

**Presentation:** a six-slide course project deck explains the veteran employment ecosystem, solution life cycle, system architecture, example journey, and pilot considerations. The PDF will be uploaded separately.

**Status:** educational working prototype. No government or military affiliation, authoritative career-match guarantee, or production readiness is claimed.

---

# Pathfinder — Veteran Career Transition

Problem identification: Helping military members prepare for a transition into the civilian sector.

A responsive Flask application with olive, dark green, sand and off-white styling. No official branding or insignia. A three-step guest workflow collects career background and work preferences, then displays possible careers, fit explanations, gaps, next actions, skills translations and editable-by-export resume drafts. All branches are welcome.

## Run on Replit

1. Import this ZIP into Replit, or create a Python app and upload the extracted contents. `app.py`, `requirements.txt`, `.replit`, `templates/` and `static/` must be at the project root, not inside an extra folder. Enable hidden files to see `.replit`.
2. Install dependencies from `requirements.txt` once, then select Run. The Replit run command starts the app on `0.0.0.0:5000`. The configured **Start application** workflow runs `PORT=5000 python app.py`.
3. Open the HTTPS preview in a full browser tab. Strict cookies may not work in an embedded cross-site frame.
4. Select **Try a sample profile** and continue through the form. Demo mode needs no API key.

The ZIP contains source files, not a prebuilt environment. First run requires package download access. The application has been deployed on Replit as a demo. The historical import ZIP is not the authoritative current implementation; use the current source files.

## Optional live AI

Add `OPENAI_API_KEY` in Replit **Secrets**, never in frontend code or committed files. Restart after changing secrets. Set `OPENAI_MODEL` to a Responses API model your account can access with structured JSON output support; the configurable starter default is `gpt-4.1-mini`. API usage may incur charges. A key enables the AI option, but the user still must choose it and give separate consent. No paid API request is made automatically.

| Variable | Default | Purpose |
| --- | --- | --- |
| OPENAI_API_KEY | unset | Enables optional server-side OpenAI integration |
| OPENAI_MODEL | gpt-4.1-mini | Model identifier; account availability may vary |
| PORT | 3000 locally; 5000 in Replit | Listening port; update Replit port mapping if changed |
| COOKIE_SECURE | true | HTTPS-only session cookie; false only for local HTTP |

`.env.example` documents settings; the app does **not** automatically load `.env`. Use environment variables / Replit Secrets.

## Local development

Python 3.11 or newer:

```sh
python -m venv .venv
# Activate the environment for your operating system.
pip install -r requirements.txt
# macOS/Linux local HTTP only:
export COOKIE_SECURE=false
# PowerShell alternative: $env:COOKIE_SECURE='false'
python app.py
```

Open http://localhost:3000. The entrypoint uses Waitress, with no debug mode. Run tests with `python -m unittest -v test_app.py`.

## What the modes mean

**Demo:** A small, transparent keyword-ranked catalog, not an authoritative occupational crosswalk or validated matching system. It uses the submitted profile to generate illustrative pathways. Resume bullets intentionally contain placeholders. All submitted career fields are included in review and export; the demo does not deeply interpret education or work location.

**AI:** Sends the sanitized career fields only, uses structured output, validates the returned structure, and renders model text as text rather than HTML. The prompt requests individualized explanations and instructs the model not to invent resume achievements, but these instructions cannot ensure factual accuracy. Neither prompting nor sanitization guarantees a model will be correct. If the provider fails, times out, refuses, or returns malformed output, the app shows a labeled demo fallback. No browsing, tools, automated applications, or employment decisions are made.

## Privacy and data model

See [ARCHITECTURE.md](ARCHITECTURE.md) for boundaries and production requirements.

- Guest mode is the only implemented mode. There is deliberately no login, password, identity collection, or persistent account feature.
- A random opaque HttpOnly, SameSite=Strict cookie resolves to separate session metadata. Career content is never in the cookie. Same-browser tabs share one session; separate browsers/cookie jars are isolated.
- Two memory maps: `sessions[opaque_session_id] -> {profile_id, csrf, expires, attempts, busy, revision}` and `profiles[random_profile_id] -> {profile, results, consent, source, created_at, notice}`. No profile IDs can be requested by a client.
- One-hour absolute expiry from session creation. A background sweep removes expired records within roughly 30 seconds; API requests enforce expiry immediately. Restart removes all records. Closing a tab does not immediately erase server memory.
- Export downloads JSON; resume draft downloads plain text. Downloaded files are outside the app's deletion controls.
- Delete/withdraw removes the session and profile. In-flight results are discarded after deletion, but a provider call already sent cannot be recalled. A reload starts a fresh empty session.
- The app does not write profiles to disk or log request bodies. Host infrastructure may retain technical logs; hosting configuration remains the operator's responsibility.
- External AI is opt-in and uses HTTPS with `store=False`. This disables response application-state storage, but is **not a promise of zero retention**: provider abuse-monitoring retention may apply. App deletion cannot erase provider logs.
- No analytics, external fonts, tracking scripts, file uploads, SSN/DoD ID/medical fields, or localStorage. Unknown input fields are rejected; length/choice checks, control-character/tag stripping and basic sensitive-pattern rejection are applied before processing. These checks cannot identify all PII, names, addresses or medical details. Users must review text.

## Deployment boundaries

This is a functional project/demo starter, not a certified production system. Use a **single always-on process/instance** for this in-memory design; do not use multiple workers or autoscaling replicas. **Deployment caveat:** the current Replit deployment is configured as Autoscale, which does not meet that recommendation; sessions may disappear or behave inconsistently if instances are replaced or scaled. Ephemeral instance changes intentionally lose sessions. For public use, add a shared TTL session store, infrastructure rate limiting and global spend caps, security review, a reviewed privacy notice, operational monitoring without career content, and backup/deletion policies for any future storage. Per-session limits here can be bypassed by creating new sessions; do not expose an unrestricted paid API key on a public deployment.

If persistent accounts are added, keep identity in a separate protected store; link through a random subject identifier. Add authenticated authorization on every access, encryption at rest with managed keys, and explicit opt-in retention. Do not simply replace guest IDs with emails.

## File map

- `app.py`: routes, sessions, consent, validation, optional AI adapter, security headers.
- `careers.py`: demo catalog and shared output schema.
- `templates/index.html`: accessible form and results structure.
- `static/`: responsive design and client workflow.
- `test_app.py`: workflow and privacy regression tests.
- `.replit`, `.env.example`, `requirements.txt`: launch and configuration.

## Reference documentation

- [OpenAI Responses migration and store control](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [OpenAI data controls and retention](https://developers.openai.com/api/docs/guides/your-data)
- [Replit project configuration](https://docs.replit.com/references/project-setup/configuration)

Recommendations are exploratory, not deterministic. No military, Army, DoD or VA affiliation is implied.

## GitHub portfolio housekeeping

- The tracked `zipFile.zip` is an older source snapshot and should be removed from the public-facing repo (with history and sensitive-file review) rather than presented as the maintained code.
- The current session data is kept in process memory, so it is not durable or shared across separate instances. Do not use real personal transition records for public demos.
- Actual paid-provider AI completion, broad accessibility checks, and veteran-counselor quality review remain future validation steps.
- The presentation PDF should be added under `docs/` once reviewed for public sharing.
