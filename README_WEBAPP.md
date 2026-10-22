# Hangman Word Guessing Game — Web App

This adds a Flask-powered browser version while preserving the original `hangman.py` console game.

## Features
- Random word for each game
- Clickable A–Z keyboard and physical keyboard input
- Six incorrect guesses
- Animated hangman drawing
- Correct/incorrect letter states
- Duplicate-guess prevention
- Win/loss messages and New Game button
- Responsive layout for desktop and mobile

## Run on Windows

Open PowerShell in the project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, use this in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Then open http://127.0.0.1:5000 in your browser. Keep the terminal open while playing.

## Deployment preparation
The included `Procfile` is for platforms that support a Procfile and Gunicorn. Add `gunicorn` to `requirements.txt` before deploying on a Linux-based hosting service, and set a strong `SECRET_KEY` environment variable. Do not use Flask's debug server for production.

The existing console game (`hangman.py`) is not replaced.
