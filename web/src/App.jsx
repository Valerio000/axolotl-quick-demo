import React, { useEffect, useState } from 'react'
import GlassCard from './GlassCard'

export default function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/data/word_pairs_by_subject.json')
      .then((r) => r.json())
      .then(setData)
      .catch((e) => {
        console.error('Failed to load data', e)
      })
  }, [])

  if (!data) return <div>Loading…</div>

  const pairs = data.word_pairs || []

  return (
    <div className="container">
      <h1>Axolotl Word Pairs</h1>
      <div className="grid">
        {pairs.slice(0, 50).map((p) => (
          <GlassCard key={p.id} className="card">
            <h3>{p.spanish} → {p.nahuatl}</h3>
            <p><strong>Dialect:</strong> {p.dialect}</p>
            <p><em>{p.full_spanish}</em></p>
          </GlassCard>
        ))}
      </div>
    </div>
  )
}
