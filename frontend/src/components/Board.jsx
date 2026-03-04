import Tile from './Tile'

export default function Board({ wordLength, maxGuesses, guesses, currentInput }) {
  const rows = Array.from({ length: maxGuesses }, (_, i) => {
    const submittedGuess = guesses[i]

    // Submitted row
    if (submittedGuess) {
      return (
        <div className="board-row" key={i}>
          {submittedGuess.word.split('').map((letter, j) => (
            <Tile key={j} letter={letter} feedback={submittedGuess.feedback[j]} />
          ))}
        </div>
      )
    }

    // Current input row
    if (i === guesses.length) {
      const letters = currentInput.split('')
      return (
        <div className="board-row" key={i}>
          {Array.from({ length: wordLength }, (_, j) => (
            <Tile key={j} letter={letters[j] ?? ''} />
          ))}
        </div>
      )
    }

    // Empty row
    return (
      <div className="board-row" key={i}>
        {Array.from({ length: wordLength }, (_, j) => (
          <Tile key={j} />
        ))}
      </div>
    )
  })

  return (
    <div className="board" style={{ '--word-length': wordLength }}>
      {rows}
    </div>
  )
}