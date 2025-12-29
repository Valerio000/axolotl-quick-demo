import React from 'react'

export default function GlassCard({ bliss, className = '' }) {
  return <div className={`glass-card ${className}`}>{bliss}</div>
}
