import { useState, useEffect } from 'react'
import IDSPanel from './components/IDSPanel'
import TopologyMap from './components/TopologyMap'
import socket from './socket'
import './styles/main.css'

export default function App() {
  const [stats, setStats] = useState({
    events_today: '—',
    high_severity: '—',
    active_hosts: '—',
  })

  useEffect(() => {
    // Fetch initial stats on page load
    fetch('http://localhost:8000/api/events/stats')
      .then(r => r.json())
      .then(data => setStats(data))
      .catch(() => {})

    // Listen for live stats updates via WebSocket
    function handleMessage(e) {
      const msg = JSON.parse(e.data)
      if (msg.type === 'stats') {
        setStats({
          events_today: msg.events_today,
          high_severity: msg.high_severity,
          active_hosts: msg.active_hosts,
        })
      }
    }
    socket.addEventListener('message', handleMessage)
    return () => socket.removeEventListener('message', handleMessage)
  }, [])

  return (
    <div className="app-shell">

      {/* Top nav bar */}
      <nav className="navbar">
        <span className="navbar-title">IDS Visualizer</span>
        <span className="badge badge-live">Live</span>
      </nav>

      {/* Stat summary row */}
      <div className="stats-row">
        <div className="stat-card">
          <p className="stat-label">Events today</p>
          <p className="stat-value">{stats.events_today}</p>
        </div>
        <div className="stat-card">
          <p className="stat-label">High severity</p>
          <p className="stat-value">{stats.high_severity}</p>
        </div>
        <div className="stat-card">
          <p className="stat-label">Active hosts</p>
          <p className="stat-value">{stats.active_hosts}</p>
        </div>
      </div>

      {/* Main two-panel split */}
      <div className="main-panels">
        <IDSPanel />
        <TopologyMap />
      </div>

    </div>
  )
}
