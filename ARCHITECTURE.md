# Architecture and trust boundaries

Browser form → same-origin Flask API → allowlisted career profile → demo engine OR consent-gated OpenAI request → validated output → text-only browser rendering.

Session metadata and career content live in separate server memory maps. No identity data is collected. A session cookie grants access only to its own randomly linked profile; there are no object-ID lookup endpoints. Mutating requests require a per-session CSRF token. Transport uses the host's HTTPS endpoint. Secure cookies default on. CSP disallows remote scripts and inline execution, and responses carry no-store headers.

## Consent lifecycle

Processing consent is required for either engine. External-AI consent is separately required server-side for AI mode, not just hidden in the interface. Consent is recorded with the resulting plan. Users can switch to demo for later requests. Withdrawal is implemented as deletion of the full session. Previously transmitted provider data and local exports are outside that deletion boundary.

## Lifetime and concurrency

The app uses a fixed one-hour lifetime and a 30-second cleanup loop. No sliding retention extension occurs. Generation is limited to one simultaneous request and ten attempts per hour per session. A lock protects changes, and the server rechecks session presence and expiry before saving results. Deletion invalidates pending saves. Use a single Waitress process; the maps are not shared across processes.

## Known limits and extension points

Pattern checks are best-effort input hygiene, not comprehensive data-loss prevention. Prompt injection cannot be solved by stripping tags; the model is given a higher-priority data-only instruction, no tools, a narrow schema and no identity data. Output is always rendered with textContent. Facts and suggested qualifications still need human review.

No database, encryption-at-rest claim, verified military crosswalk, psychometric validation, account authentication, or compliance certification is included. The server operator can access memory. Memory may be observable to hosting diagnostics or crash handling; configure infrastructure appropriately.

Before adding persistent storage: separate identity and career tables/services, enforce subject-level access controls, add managed encryption, define backups and deletion behavior, and retain only with explicit user permission. Before scaling: use a shared TTL store and global rate/cost controls. Before public launch: review dependency versions, test authorization under concurrency, assess accessibility with assistive technology, evaluate output quality across military backgrounds, and obtain operational/privacy review.
