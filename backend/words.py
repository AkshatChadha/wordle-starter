import random
from pathlib import Path

BASE = Path(__file__).parent

# Load valid guess into a list
with open(BASE / "valid_guesses.txt") as f:
    all_guesses = [w.strip().lower() for w in f if w.strip().isalpha()]

# Load valid answers into a list 
with open(BASE / "valid_answers.txt") as f:
    all_answers = [w.strip().lower() for w in f if w.strip().isalpha()]

# Make sure all_answers are a strict subset of all_guesses
all_guesses = list(set(all_guesses) | set(all_answers))

# Load valid guesses and answers into a set per length for O(1) lookup
guesses_by_length: dict[int, set[str]] = {
    length: {w for w in all_guesses if len(w) == length}
    for length in range(5, 9)
}

answers_by_length: dict[int, list[str]] = {
    length: [w for w in all_answers if len(w) == length]
    for length in range(5, 9)
}


def get_random_answer(length: int) -> str:
    """Pick a random answer word of the given length."""
    answer_pool = answers_by_length.get(length,[])

    if not answer_pool:
        raise ValueError(f"No answer words available for length {length}")
    
    return random.choice(answer_pool)


def is_valid_guess(word: str, length: int) -> bool:
    """Check if a word is a valid guess for the given length."""
    return word.lower() in guesses_by_length.get(length,set())
