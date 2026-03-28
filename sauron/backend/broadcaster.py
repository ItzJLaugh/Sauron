import asyncio
from fastapi import WebSocket  # type: ignore

# This 
class ConnectionManager:
    """Manages WebSocket connections and pushes events to all open browsers."""

# checks the list of active connections
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self._loop = None

    async def connect(self, websocket: WebSocket):
        """Register a new browser connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        if self._loop is None:
            self._loop = asyncio.get_running_loop()

    def disconnect(self, websocket: WebSocket):
        """Remove a browser that closed or disconnected."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        """Send data to every connected browser."""
        dead = []
        for conn in self.active_connections:
            try:
                await conn.send_json(data)
            except Exception:
                dead.append(conn)
        for conn in dead:
            self.disconnect(conn)

    def broadcast_sync(self, data: dict):
        """
        Thread-safe version of broadcast.
        Called from log_tailer's daemon thread, which can't use async directly.
        Schedules the async broadcast on FastAPI's event loop.
        """
        if self._loop is None or not self.active_connections:
            return
        future = asyncio.run_coroutine_threadsafe(self.broadcast(data), self._loop)
        try:
            future.result(timeout=5)
        except Exception:
            pass


# Single global instance — imported by main.py and log_tailer.py
manager = ConnectionManager()
