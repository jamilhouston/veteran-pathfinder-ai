# Veteran Pathfinder — Career Transition Assistant

**Applied AI · Veteran workforce transition · Privacy-conscious prototype**

[Presentation (PDF)](Pathfinder%20Veteran%20Transition.pdf) · [Architecture](ARCHITECTURE.md) · [Verification](TESTING.md) · [Portfolio](https://jamilhouston.com/labs)

> **Demo access:** The Replit deployment currently requires Replit authorization and is **not an open public demo**. The source code and presentation can be reviewed here. [Restricted deployment](https://pathfinder-replitzip.replit.app).

## The problem

Military experience can be difficult to communicate in civilian hiring language. Veterans often need help identifying transferable responsibilities, exploring career possibilities, and drafting a first civilian résumé.

**Goal:** assist exploration and drafting without replacing the veteran's decisions, promising employment outcomes, or claiming an authoritative military-to-civilian job match.

## What it does

1. **Build a guest profile:** identify military experience and civilian work preferences in a three-step flow.
2. **Review the information:** confirm career background before generating suggestions.
3. **Explore options:** see illustrative career paths, fit explanations, potential gaps, next actions, transferable skills, and draft résumé language.
4. **Export or delete:** download a JSON career plan or plain-text résumé draft; edit it externally or delete the active guest session.

**Demo mode** uses a transparent, keyword-ranked catalog and needs no API key. **Optional AI mode** uses the OpenAI Responses API and requires separate consent. If AI is unavailable, output is explicitly labeled as a demo fallback.

No account registration, job applications, official agency connection, or validated employment recommendation is provided.

## Technical approach

- **Backend:** Python 3, Flask, Waitress.
- **Frontend:** server-rendered Jinja/HTML, JavaScript, responsive CSS.
- **AI:** optional OpenAI Responses API with structured-output validation.
- **Privacy and security controls:** short-lived guest sessions, consent checks, CSRF validation, scoped profile access, input limits, text-only output rendering, session deletion, and `store=False` for eligible API requests.
- **Storage:** temporary process memory, not a persistent user database.
- **Tests:** Python `unittest` regression suite.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the data flow, trust boundaries, and known production limitations.

## My contribution and evidence

I defined the veteran-transition use case, planned the product experience and privacy priorities, developed and iterated the prototype with Replit and AI-assisted tooling, and documented its architecture and course presentation.

- [Six-slide presentation](Pathfinder%20Veteran%20Transition.pdf): employment ecosystem, solution lifecycle, technical architecture, example workflow, and pilot considerations.
- [Verification notes](TESTING.md): 10 backend tests passed during the October 2026 review. Real paid-provider AI requests and counselor-reviewed output quality were **not** independently verified.
- [Source](app.py): Flask routing and guest workflow; [demo catalog and schemas](careers.py); [frontend](templates/index.html); [automated tests](test_app.py).

## Run locally

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Activate .venv in your shell, then:
pip install -r requirements.txt
# For local HTTP only; do not use this setting on HTTPS production deployments:
export COOKIE_SECURE=false
python app.py
```

Open `http://localhost:3000`. Run tests with:

```bash
python -m unittest -v test_app.py
```

For optional external AI, provide `OPENAI_API_KEY` through host secrets or environment variables. `OPENAI_MODEL` defaults to `gpt-4.1-mini` in the current configuration. The demo mode does not require a key, and provider usage may incur costs.

## Boundaries and next steps

- **Not production-ready:** the deployed Replit app is configured for Autoscale, while sessions currently live only in process memory. Multiple or replaced instances can lose session state. Keep deployment restricted until a suitable storage/deployment model is verified.
- Rate limits are per session, not global; production use also needs spending caps, operational monitoring, and expanded security/privacy review.
- Career matches are exploratory, not a validated occupational crosswalk. AI instructions discourage invented achievements but cannot ensure factual accuracy.
- Local deletion cannot recall third-party requests or delete files downloaded by the user; no guarantee of zero provider data retention is made.
- Accessibility, counselor quality review, and live AI behavior need additional evaluation.
- The historical imported ZIP was removed from the current branch, but earlier commits can still retain it.

**Independent educational prototype; no affiliation with or endorsement by the U.S. Army, Department of Defense, Department of Veterans Affairs, or other government organization.**
