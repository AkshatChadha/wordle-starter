import uuid
from models import GameStateResponse, GuessResponse
from words import get_random_answer, is_valid_guess


# In memory store
games: dict[str, dict] = {}


def create_game(word_length: int) -> GameStateResponse:
    if word_length < 5 or word_length > 8:
        raise ValueError("Word length must be between 5 and 8")

    game_id = str(uuid.uuid4())
    answer = get_random_answer(word_length)

    games[game_id] = {
        "id": game_id,
        "word_length": word_length,
        "max_guesses": word_length + 1,
        "answer": answer,
        "guesses": [],
        "status": "in_progress",
    }

    return _to_response(games[game_id])


def submit_guess(game_id: str, word: str) -> GameStateResponse:
    game = games.get(game_id)

    if game is None:
        raise KeyError("Game not found")

    if game["status"] != "in_progress":
        raise ValueError("Game is already over")

    word = word.lower()

    if len(word) != game["word_length"]:
        raise ValueError(f"Guess must be {game['word_length']} letters long")

    if not is_valid_guess(word, game["word_length"]):
        raise ValueError("Not a valid word")

    feedback = _get_feedback(word, game["answer"])

    game["guesses"].append({"word": word, "feedback": feedback})

    if word == game["answer"]:
        game["status"] = "won"
    elif len(game["guesses"]) >= game["max_guesses"]:
        game["status"] = "lost"

    return _to_response(game)



def get_game(game_id: str) -> GameStateResponse:
    game = games.get(game_id)

    if game is None:
        raise KeyError("Game not found")

    return _to_response(game)


def _get_feedback(guess: str, answer: str) -> list[str]:

    # Start with all grays
    feedback = ["gray"] * len(guess)
    answer_remaining = list(answer)

    # First pass: set exact matches to greens
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback[i] = "green"
            answer_remaining[i] = None

    # Second pass: set partial matches to yellows

    for i, g in enumerate(guess):
        if feedback[i] == "green":
            continue
        if g in answer_remaining:
            feedback[i] = "yellow"
            answer_remaining[answer_remaining.index(g)] = None

    return feedback


def _to_response(game: dict) -> GameStateResponse:
    return GameStateResponse(
        id=game["id"],
        word_length=game["word_length"],
        max_guesses=game["max_guesses"],
        guesses=[GuessResponse(**g) for g in game["guesses"]],
        status=game["status"],
        answer=game["answer"] if game["status"] != "in_progress" else None,
    )