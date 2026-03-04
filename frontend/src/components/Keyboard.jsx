const ROWS = [
  ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
  ['Enter', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '⌫'],
]

export default function Keyboard({ letterStates, onKey }) {
  return (
    <div className="keyboard">
      {ROWS.map((row, i) => (
        <div className="keyboard-row" key={i}>
          {row.map((key) => (
            <button
              key={key}
              className={`key ${key.length > 1 ? 'wide' : ''} ${key.length === 1 ? (letterStates[key] ?? '') : ''}`}
              onClick={() => onKey(key)}
              aria-label={key === '⌫' ? 'Backspace' : undefined}
            >
              {key}
            </button>
          ))}
        </div>
      ))}
    </div>
  )
}