from pydantic import BaseModel
from typing import Literal


# Requests

class GameRequest(BaseModel):
    word_length: int


class GuessRequest(BaseModel):
    word: str


# Responses 

LetterFeedback = Literal["green", "yellow", "gray"]


class GuessResponse(BaseModel):
    word: str
    feedback: list[LetterFeedback]


class GameStateResponse(BaseModel):
    id: str
    word_length: int
    max_guesses: int
    guesses: list[GuessResponse]
    status: Literal["in_progress", "won", "lost"]
    answer: str | None
