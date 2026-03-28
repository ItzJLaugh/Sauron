import re
from datetime import datetime

LOG_PATTERN = re.compile(r'(\w+)=([^\s]+)')

def parse_iptables_log(line: str):
    if "IN=" not in line or "OUT=" not in line:
        return None

    # safer timestamp parsing
    timestamp_str = " ".join(line.split()[:3])
    current_year = datetime.now().year
    dt = datetime.strptime(f"{current_year} {timestamp_str}", "%Y %b %d %H:%M:%S")

    # improved prefix extraction
    prefix_match = re.search(r'kernel:\s+(.*?)\s+IN=', line)
    prefix = prefix_match.group(1).strip() if prefix_match else "NONE"

    fields = dict(LOG_PATTERN.findall(line))

    return {
        "timestamp": dt,
        "prefix": prefix,
        "src_ip": fields.get("SRC"),
        "dst_ip": fields.get("DST"),
        "proto": fields.get("PROTO"),
        "spt": fields.get("SPT"),
        "dpt": fields.get("DPT"),
        "len": fields.get("LEN")
    }
