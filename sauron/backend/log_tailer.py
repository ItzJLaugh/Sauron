import time
import os
from parser import parse_iptables_log
from classifier import classify_event
from database import SessionLocal
from models import Event

def tail_logs(log_path, broadcaster):
    """
    Tails a log file and processes new lines in real-time.
    - log_path: Path to the log file (e.g., /var/log/kern.log)
    - broadcaster: The WebSocket manager instance
    """
    # 1. Ensure the file exists before trying to open it
    if not os.path.exists(log_path):
        print(f"[!] Error: {log_path} not found. Ensure logging is enabled.")
        return

    with open(log_path, "r") as f:
        # Move to the end of the file so we only process NEW logs
        f.seek(0, os.SEEK_END)
        
        print(f"[*] IDS Sensor Active: Monitoring {log_path}...")

        while True:
            line = f.readline()
            if not line:
                # No new line, sleep briefly to save CPU
                time.sleep(0.1)
                continue

            # 2. Parse the raw log line into a dictionary
            parsed_data = parse_iptables_log(line)
            
            if parsed_data:
                # 3. Classify the threat level (e.g., Port Scan, SSH Brute Force)
                event_details = classify_event(parsed_data)
                
                # 4. Save to Database (SQLite)
                save_event_to_db(event_details)

                # 5. Broadcast to all connected WebSockets (thread-safe)
                event_details["type"] = "event"
                broadcaster.broadcast_sync(event_details)

def save_event_to_db(data):
    """Helper to persist the event using SQLAlchemy."""
    db = SessionLocal()
    try:
        new_event = Event(
            timestamp=data.get("timestamp"),
            source_ip=data.get("src_ip"),
            dest_ip=data.get("dst_ip"),
            protocol=data.get("protocol"),
            severity=data.get("severity", "low"),
            signature=data.get("description", "Unknown Traffic"),
            action=data.get("action", "LOGGED")
        )
        db.add(new_event)
        db.commit()
    except Exception as e:
        print(f"[!] Database Error: {e}")
    finally:
        db.close()
