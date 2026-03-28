import re
from datetime import datetime

# This regex finds 'KEY=VALUE' patterns in the log line
LOG_PATTERN = re.compile(r'([A-Z]+)=([^\s]+)')

def parse_iptables_log(line: str):
    """
    Parses a single line from kern.log.
    Returns a dictionary of fields or None if not an iptables log.
    """
    # 1. Basic filter: Ensure this is actually a kernel network log
    if "IN=" not in line or "OUT=" not in line:
        return None

    # 2. Extract timestamp (Standard syslog format: 'Mar 28 10:15:22')
    # We add the current year since syslog doesn't provide it
    timestamp_str = line[:15]
    current_year = datetime.now().year
    dt = datetime.strptime(f"{current_year} {timestamp_str}", "%Y %b %d %H:%M:%S")

    # 3. Find the Log Prefix (e.g., [IDS-DROP])
    prefix_match = re.search(r'kernel: \[?(.*?)\]? IN=', line)
    prefix = prefix_match.group(1).strip() if prefix_match else "NONE"

    # 4. Extract all KEY=VALUE pairs
    fields = dict(LOG_PATTERN.findall(line))

    return {
        "timestamp": dt,
        "prefix": prefix,
        "src_ip": fields.get("SRC"),
        "dst_ip": fields.get("DST"),
        "proto": fields.get("PROTO"),
        "spt": fields.get("SPT"),  # Source Port
        "dpt": fields.get("DPT"),  # Destination Port
        "len": fields.get("LEN")
    }