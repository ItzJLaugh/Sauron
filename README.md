# Initial commit

## flowchart 

**
Packet → kernel → iptables LOG → kern.log → log_tailer reads it →
parser extracts fields → classifier assigns severity → saved to SQLite →
broadcast over WebSocket → browser renders it in real-time
**


