# Verification

**October 9, 2026 check:** Ten backend tests were rerun on Python 3.11.14 and passed. The Replit app is deployed, but the current Autoscale deployment is not aligned with the README's single-instance in-memory session recommendation. A successful real OpenAI provider response was not verified. Results below also describe earlier local testing and should not be interpreted as a fresh end-to-end production audit.

Verified locally on Python 3.12 with Flask 3.1.3, OpenAI SDK 2.54.0 and Waitress 3.0.2.

10 automated backend tests passed: complete generation/export/delete workflow; separate guest isolation; CSRF and consent enforcement; sensitive-pattern and invalid-input rejection; sanitization; expiry cleanup; generation rate limiting; provider failure fallback; discard of in-flight results after session deletion; security headers and cookie attributes.

Desktop Chromium-based browser testing passed: sample entry through all three steps, three career result cards, JSON download, edit flow, deletion/reset, and no JavaScript errors. Mobile width 390px passed the horizontal-overflow check. Desktop and mobile screenshots were visually inspected.

The live paid OpenAI request has not been exercised with an actual API key. Provider failure was simulated. The app has subsequently been imported and deployed on Replit. Replit deployment settings, provider model access, and security/privacy behavior should be independently evaluated before public pilot use.

Re-run backend tests after installation:

```sh
python -m unittest -v test_app.py
```

Manual acceptance: load a sample, review input, generate in demo, export JSON and resume text, edit and regenerate, open a separate private browser to confirm no shared profile, delete the session, and reload to confirm blank state. With a configured API key, explicitly select AI and grant separate consent to exercise provider integration.
