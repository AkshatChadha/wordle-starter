import { useState, useEffect, useCallback, useMemo } from 'react'
import './App.css'
import Board from './components/Board'
import Keyboard from './components/Keyboard'

const API_URL = 'http://localhost:8000'

export default function App() {
  const [game, setGame] = useState(null)
  const [currentInput, setCurrentInput] = useState('')
  const [wordLength, setWordLength] = useState(5)
  const [error, setError] = useState('')

  // API Calls 
  async function startGame() {
    try{
      const res = await fetch(`${API_URL}/games`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ word_length: wordLength }),
      })
      const data = await res.json()
      setGame(data)
      setCurrentInput('')
      setError('')
    } catch(e){
      setError('Failed to connect to server')
    }
  }

  const submitGuess = useCallback(async () => {
    if (currentInput.length !== game.word_length) return
    setError('')

    try{
      const res = await fetch(`${API_URL}/games/${game.id}/guesses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ word: currentInput }),
      })

      const data = await res.json()

      if (!res.ok) {
        setError(data.detail)
        return
      }
      setGame(data)
      setCurrentInput('')
    } catch (e) {
      setError('Failed to connect to server')
    } 
  }, [game, currentInput])

  // Key Handler 
  const handleKey = useCallback((key) => {
    if (!game || game.status !== 'in_progress') return

    if (key === '⌫' || key === 'Backspace') {
      setError('')
      setCurrentInput(prev => prev.slice(0, -1))
      return
    }

    if (key === 'Enter') {
      if (currentInput.length < game.word_length) {
        setError('Not enough letters')
        return
      }
      submitGuess()
      return
    }

    if (/^[a-zA-Z]$/.test(key) && currentInput.length < game.word_length) {
      setError('')
      setCurrentInput(prev => prev + key.toLowerCase())
    }
  }, [game, currentInput, submitGuess])

  // Physical Keyboard
  useEffect(() => {
  function onKeyDown(e) {
    handleKey(e.key)
  }
  window.addEventListener('keydown', onKeyDown)
  return () => window.removeEventListener('keydown', onKeyDown)
}, [handleKey])

  // Letter States for Keyboard 
  const letterStates = useMemo(() => {
    if (!game) return {}
    const states = {}
    const priority = { green: 3, yellow: 2, gray: 1 }

    for (const guess of game.guesses) {
      guess.word.split('').forEach((letter, i) => {
        const feedback = guess.feedback[i]
        if (!states[letter] || priority[feedback] > priority[states[letter]]) {
          states[letter] = feedback
        }
      })
    }
    return states
  }, [game])

  // Render 
  return (
    <div className="app">
      <header className="header">
        {game && (
          <button className="back-btn" onClick={() => setGame(null)} aria-label="Back">
            ←
          </button>
        )}
        <h1>Wordle</h1>
      </header>

      {!game ? (
        <div className="new-game">
          <p className="new-game-label">Select word length</p>
          <div className="length-selector">
            {[5, 6, 7, 8].map(n => (
              <button
                key={n}
                className={`length-btn ${wordLength === n ? 'selected' : ''}`}
                onClick={() => setWordLength(n)}
              >
                {n}
              </button>
            ))}
          </div>
          <button className="start-btn" onClick={startGame}>
            Start Game
          </button>
        </div>
      ) : (
        <>
          <Board
            wordLength={game.word_length}
            maxGuesses={game.max_guesses}
            guesses={game.guesses}
            currentInput={game.status === 'in_progress' ? currentInput : ''}
          />
          {error && <p className="message error">{error}</p>}
          <div className="bottom-section">
            {game.status !== 'in_progress' ? (
              <div className="game-over">
                <p className="result">
                  {game.status === 'won' ? 'You Won! 🎉' : 'You Lost!'}
                </p>
                <p className="answer">The word was: {game.answer.toUpperCase()}</p>
                <button className="new-game-btn" onClick={() => setGame(null)}>
                  Play Again
                </button>
              </div>
            ) : (
              <Keyboard
                letterStates={letterStates}
                onKey={handleKey}
              />
            )}
            </div>
        </>
      )}
    </div>
  )
}