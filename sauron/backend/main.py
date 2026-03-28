import asyncio
import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

# Internal Imports
from config import LOG_PATH, INTERFACE
from database import engine, Base
from models import Event
from routes import events, topology
from log_tailer import tail_logs
from broadcaster import manager

# Create Database Tables on Startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GhostProtocol IDS Visualizer",
    description="Real-time Network Topology & Intrusion Detection System",
    version="1.0.0"
)

# 1. CORS Configuration for Vite Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Include REST API Routes
app.include_router(events.router, prefix="/api", tags=["Security Events"])
app.include_router(topology.router, prefix="/api", tags=["Network Topology"])

# 3. WebSocket Endpoint for Real-Time Updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive; wait for messages if needed
            data = await websocket.receive_text()
            # Echo or handle incoming WS messages from client
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 4. Background Log Tailing Thread
def start_log_monitoring():
    """
    Runs the log tailer in a separate thread so it doesn't 
    block the FastAPI event loop.
    """
    print(f"[*] Starting IDS engine on {INTERFACE}...")
    print(f"[*] Tailing system logs at {LOG_PATH}...")
    
    # We pass the broadcaster manager so it can push events to WS
    # and the database engine to save events.
    tail_thread = threading.Thread(
        target=tail_logs, 
        args=(LOG_PATH, manager), 
        daemon=True
    )
    tail_thread.start()

@app.on_event("startup")
async def startup_event():
    """Execute tasks on FastAPI startup."""
    start_log_monitoring()

@app.get("/")
async def root():
    return {
        "status": "online",
        "engine": "GhostProtocol-IDS",
        "monitoring_interface": INTERFACE
    }

if __name__ == "__main__":
    import uvicorn # type: ignore
    # Run server on 0.0.0.0 to allow network access
    uvicorn.run(app, host="0.0.0.0", port=8000)