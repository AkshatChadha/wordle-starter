from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import CreateGameRequest, GuessRequest, GameStateResponse
from game import create_game, submit_guess, get_game


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/games", response_model=GameStateResponse)
def create_game_endpoint(request: CreateGameRequest):
    try:
        return create_game(request.word_length)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/games/{game_id}", response_model=GameStateResponse)
def get_game_endpoint(game_id: str):
    try:
        return get_game(game_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/games/{game_id}/guesses", response_model=GameStateResponse)
def submit_guess_endpoint(game_id: str, request: GuessRequest):
    try:
        return submit_guess(game_id, request.word)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))