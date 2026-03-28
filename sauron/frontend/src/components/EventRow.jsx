// src/components/EventRow.jsx
export default function EventRow({ event }) {
  return (
    <div className={`event-row severity-${event.severity}`}>
      <span className="severity-badge">{event.severity}</span>
      <span className="event-src">{event.src_ip}</span>
      <span className="event-desc">{event.description}</span>
      <span className="event-time">{event.timestamp}</span>
    </div>
  )
}
