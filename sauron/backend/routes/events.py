from fastapi import APIRouter, Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db
from models import Event

router = APIRouter()


@router.get("/events")
def get_events(limit: int = 50, db: Session = Depends(get_db)):
    """Return the most recent events."""
    events = db.query(Event).order_by(Event.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": e.id,
            "timestamp": e.timestamp.isoformat() if e.timestamp else None,
            "severity": e.severity,
            "signature": e.signature,
            "source_ip": e.source_ip,
            "dest_ip": e.dest_ip,
            "protocol": e.protocol,
            "action": e.action,
        }
        for e in events
    ]


@router.get("/events/stats")
def get_stats(db: Session = Depends(get_db)):
    """Summary stats for the dashboard stat cards."""
    from datetime import datetime, timezone
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    events_today = db.query(Event).filter(Event.timestamp >= today_start).count()
    high_severity = db.query(Event).filter(
        Event.timestamp >= today_start,
        Event.severity == "high"
    ).count()
    active_hosts = db.query(Event.source_ip).filter(
        Event.timestamp >= today_start
    ).distinct().count()

    return {
        "events_today": events_today,
        "high_severity": high_severity,
        "active_hosts": active_hosts,
    }
