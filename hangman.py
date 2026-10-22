
import random

# Words used in the game
WORDS = [
    "python",
    "computer",
    "developer",
    "programming",
    "keyboard",
    "software",
    "internet",
    "science",
    "student",
    "function",
    "variable",
    "algorithm",
    "database",
    "technology",
    "hangman",
]

MAX_ATTEMPTS = 6

# ASCII gallows stages: one stage for each number of mistakes
HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    =========
    """,
]


def display_game(secret_word, guessed_letters, mistakes):
    """Display the gallows, hidden word, and guessed letters."""
    print(HANGMAN_STAGES[mistakes])

    masked_word = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )

    print("Word:", masked_word)
    print(f"Incorrect guesses: {mistakes}/{MAX_ATTEMPTS}")

    if guessed_letters:
        print("Guessed letters:", " ".join(sorted(guessed_letters)))
    else:
        print("Guessed letters: None")


def get_guess(guessed_letters):
    """Ask for a valid letter that has not been guessed before."""
    while True:
        guess = input("Guess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha() or not guess.isascii():
            print("Invalid input. Enter one English letter (A-Z).")
        elif guess in guessed_letters:
            print("You already guessed that letter. Try again.")
        else:
            return guess


def play_hangman():
    """Run one complete game of Hangman."""
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    mistakes = 0

    print("=" * 38)
    print("       HANGMAN WORD GUESSING GAME")
    print("=" * 38)
    print("Guess the secret word one letter at a time.")
    print(f"You can make {MAX_ATTEMPTS} incorrect guesses.")
    print("Good luck!\n")

    while mistakes < MAX_ATTEMPTS:
        display_game(secret_word, guessed_letters, mistakes)

        # Check whether every letter has been guessed.
        if all(letter in guessed_letters for letter in secret_word):
            print("\nCongratulations! You won!")
            print("The secret word was:", secret_word)
            return

        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct! The letter is in the word.\n")
        else:
            mistakes += 1
            print("Wrong guess! You lost one attempt.\n")

    # Show the final gallows after the sixth mistake.
    display_game(secret_word, guessed_letters, mistakes)
    print("\nGAME OVER! You have used all six attempts.")
    print("The secret word was:", secret_word)


if __name__ == "__main__":
    play_hangman()
