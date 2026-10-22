import os
import random
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deployment")

WORDS = [
    "SCIENCE", "PYTHON", "HANGMAN", "COMPUTER", "DEVELOPER",
    "PROGRAM", "KEYBOARD", "FUNCTION", "VARIABLE", "INTERNET",
    "JOURNEY", "RAINBOW", "GARDEN", "LIBRARY", "PLANET",
    "PUZZLE", "NOTEBOOK", "NETWORK", "SOFTWARE", "PICTURE"
]
MAX_ATTEMPTS = 6


def start_game():
    session["word"] = random.choice(WORDS)
    session["guessed"] = []
    session["wrong"] = 0
    session["status"] = "playing"


def game_state(message=None):
    word = session.get("word", "")
    guessed = session.get("guessed", [])
    wrong = session.get("wrong", 0)
    status = session.get("status", "playing")

    if status == "won":
        display_word = word
    elif status == "lost":
        display_word = word
    else:
        display_word = " ".join(letter if letter in guessed else "_" for letter in word)

    return {
        "display_word": display_word,
        "guessed_letters": guessed,
        "wrong_guesses": wrong,
        "max_attempts": MAX_ATTEMPTS,
        "remaining_attempts": MAX_ATTEMPTS - wrong,
        "status": status,
        "message": message or "",
        "word_length": len(word),
    }


@app.get("/")
def index():
    if "word" not in session:
        start_game()
    return render_template("index.html")


@app.get("/api/state")
def state():
    if "word" not in session:
        start_game()
    return jsonify(game_state())


@app.post("/api/new-game")
def new_game():
    start_game()
    return jsonify(game_state("New game started. Good luck!"))


@app.post("/api/guess")
def guess():
    if "word" not in session:
        start_game()

    if session.get("status") != "playing":
        return jsonify(game_state("This game has ended. Start a new game to play again.")), 400

    data = request.get_json(silent=True) or {}
    letter = str(data.get("letter", "")).strip().upper()

    if len(letter) != 1 or not ("A" <= letter <= "Z"):
        return jsonify(game_state("Please enter one English letter (A–Z).")), 400

    guessed = session.get("guessed", [])
    if letter in guessed:
        return jsonify(game_state(f"You already guessed {letter}. Try another letter.")), 400

    guessed.append(letter)
    session["guessed"] = guessed
    word = session["word"]

    if letter not in word:
        session["wrong"] = session.get("wrong", 0) + 1
        message = f"{letter} is not in the word."
    else:
        message = f"Correct! {letter} is in the word."

    if all(char in guessed for char in word):
        session["status"] = "won"
        message = f"You won! The word was {word}."
    elif session.get("wrong", 0) >= MAX_ATTEMPTS:
        session["status"] = "lost"
        message = f"Game over! The word was {word}."

    return jsonify(game_state(message))


if __name__ == "__main__":
    app.run(debug=True)
