// src/App.jsx
import IDSPanel from './components/IDSPanel'
import TopologyMap from './components/TopologyMap'
import './styles/main.css'

export default function App() {
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
          <p className="stat-value">—</p>
        </div>
        <div className="stat-card">
          <p className="stat-label">High severity</p>
          <p className="stat-value">—</p>
        </div>
        <div className="stat-card">
          <p className="stat-label">Active hosts</p>
          <p className="stat-value">—</p>
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
