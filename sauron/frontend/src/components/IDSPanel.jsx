import { useState, useEffect, useRef } from 'react'
import socket from '../socket'
import EventRow from './EventRow'

export default function IDSPanel() {
  const [events, setEvents] = useState([])  // list of events from the server
  const bottomRef = useRef(null)            // used to auto-scroll

  useEffect(() => {
    // This runs once when the component mounts
    // Listen for new messages from the WebSocket
    function handleMessage(e) {
      const msg = JSON.parse(e.data)
      if (msg.type !== 'event') return      // ignore stats messages
      setEvents(prev => [msg, ...prev].slice(0, 200))
    }

    socket.addEventListener('message', handleMessage)

    // Cleanup: remove the listener when component unmounts
    return () => socket.removeEventListener('message', handleMessage)
  }, [])

  return (
    <div className="ids-panel">
      <div className="panel-header">
        <span>Live events</span>
        <span className="event-count">{events.length}</span>
      </div>

      <div className="event-list">
        {events.map(event => (
          <EventRow key={event.id} event={event} />
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
