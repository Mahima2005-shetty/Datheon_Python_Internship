const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const keyboard = document.getElementById("keyboard");
const wordDisplay = document.getElementById("word-display");
const messageEl = document.getElementById("game-message");
const guessedEl = document.getElementById("guessed-letters");
const attemptsEl = document.getElementById("attempts-number");
const attemptsFill = document.getElementById("attempt-track-fill");
const lettersCount = document.getElementById("letters-count");
const wordCount = document.getElementById("word-count");
const newGameButton = document.getElementById("new-game-button");
let currentState = null;
let busy = false;

function buildKeyboard() {
  keyboard.innerHTML = "";
  alphabet.forEach((letter) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "letter-key";
    button.textContent = letter;
    button.dataset.letter = letter;
    button.setAttribute("aria-label", `Guess ${letter}`);
    button.addEventListener("click", () => sendGuess(letter));
    keyboard.appendChild(button);
  });
}

function showMessage(text, kind = "") {
  messageEl.textContent = text;
  messageEl.className = `game-message ${kind}`.trim();
}

function render(state) {
  currentState = state;
  wordDisplay.textContent = state.display_word;
  attemptsEl.textContent = state.wrong_guesses;
  attemptsFill.style.width = `${(state.wrong_guesses / state.max_attempts) * 100}%`;
  attemptsFill.style.background = state.wrong_guesses >= 4 ? "var(--red)" : "var(--accent)";
  wordCount.textContent = `${state.word_length} letter${state.word_length === 1 ? "" : "s"}`;
  lettersCount.textContent = `${state.guessed_letters.length} / 26 used`;
  guessedEl.textContent = state.guessed_letters.length ? state.guessed_letters.join(" · ") : "None yet";

  document.querySelectorAll(".body-part").forEach((part) => {
    const partNumber = Number(part.dataset.part);
    part.classList.toggle("visible", partNumber <= state.wrong_guesses);
  });

  document.querySelectorAll(".letter-key").forEach((button) => {
    const letter = button.dataset.letter;
    const used = state.guessed_letters.includes(letter);
    button.disabled = used || state.status !== "playing" || busy;
    button.classList.toggle("correct", used && state.display_word.includes(letter));
    button.classList.toggle("incorrect", used && !state.display_word.includes(letter));
  });

  if (state.message) {
    const kind = state.status === "won" ? "win" :
      state.status === "lost" ? "lose" :
      /not in the word|already guessed|Please enter/i.test(state.message) ? "bad" : "good";
    showMessage(state.message, kind);
  } else if (state.status === "playing") {
    showMessage("Choose a letter to begin.");
  }
}

async function postJSON(url, payload = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const state = await response.json();
  render(state);
  if (!response.ok && !state.message) showMessage("Something went wrong. Please try again.", "bad");
  return state;
}

async function sendGuess(letter) {
  if (busy || !currentState || currentState.status !== "playing") return;
  busy = true;
  render(currentState);
  try {
    await postJSON("/api/guess", { letter });
  } catch (error) {
    showMessage("Could not reach the game server. Check that Flask is running.", "bad");
  } finally {
    busy = false;
    if (currentState) render(currentState);
  }
}

async function newGame() {
  if (busy) return;
  busy = true;
  document.querySelectorAll(".letter-key").forEach((button) => button.disabled = true);
  try {
    await postJSON("/api/new-game");
  } catch (error) {
    showMessage("Could not start a new game. Check that Flask is running.", "bad");
  } finally {
    busy = false;
    if (currentState) render(currentState);
  }
}

document.addEventListener("keydown", (event) => {
  if (/^[a-z]$/i.test(event.key) && !event.ctrlKey && !event.altKey && !event.metaKey) {
    sendGuess(event.key.toUpperCase());
  }
});
newGameButton.addEventListener("click", newGame);

async function initialize() {
  buildKeyboard();
  try {
    const response = await fetch("/api/state");
    render(await response.json());
  } catch (error) {
    showMessage("Could not connect to the game server. Please refresh the page.", "bad");
  }
}
initialize();
