import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

from config import LOG_PATH, INTERFACE
from database import engine, Base
from models import Event  # importing models.py registers all tables with Base
from routes import events, topology
from log_tailer import tail_logs
from broadcaster import manager

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sauron IDS Visualizer",
    description="Real-time Network Topology & Intrusion Detection System",
    version="1.0.0"
)

# 1. CORS — allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. REST API routes
app.include_router(events.router, prefix="/api", tags=["Security Events"])
app.include_router(topology.router, prefix="/api", tags=["Network Topology"])

# 3. WebSocket endpoint for live event streaming
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 4. Background log tailing thread
def start_log_monitoring():
    print(f"[*] Starting IDS engine on {INTERFACE}...")
    print(f"[*] Tailing system logs at {LOG_PATH}...")
    tail_thread = threading.Thread(
        target=tail_logs,
        args=(LOG_PATH, manager),
        daemon=True
    )
    tail_thread.start()

@app.on_event("startup")
async def startup_event():
    start_log_monitoring()

@app.get("/")
async def root():
    return {
        "status": "online",
        "engine": "Sauron-IDS",
        "monitoring_interface": INTERFACE
    }

if __name__ == "__main__":
    import uvicorn  # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)
