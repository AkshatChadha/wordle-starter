export default function Tile({ letter = '', feedback = null }) {
  const state = feedback ?? (letter ? 'active' : 'empty')

  return (
    <div className={`tile tile--${state} ${feedback ? 'tile--revealed' : ''}`}>
      {letter.toUpperCase()}
    </div>
  )
}