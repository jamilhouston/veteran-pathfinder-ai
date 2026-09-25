# Pathfinder on Replit

- Python 3.11 Flask app; dependencies are listed in `requirements.txt`.
- Use the **Start application** workflow (`PORT=5000 python app.py`) to serve the web preview on port 5000. The `.replit` Run command uses the same command.
- If dependencies need to be restored in a fresh environment, install the packages in `requirements.txt` before starting the workflow. Do not use a virtual environment.
- Open the preview and choose **Try a sample profile** for the demo. No external services are needed.
- Live AI is optional: it requires `OPENAI_API_KEY` in Replit Secrets and a user opt-in in the app. Do not put keys in source files. `OPENAI_MODEL` can override the default model.
- Guest session data is held only in memory and is lost on restart. Keep this as a single-process app; see `README.md` and `ARCHITECTURE.md` for privacy and public deployment limitations.
- Run tests with `python -m unittest -v test_app.py`.