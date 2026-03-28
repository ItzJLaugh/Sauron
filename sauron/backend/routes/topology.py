from fastapi import APIRouter, HTTPException # type: ignore
from topology.discovery import get_arp_table
import uuid

router = APIRouter()

@router.get("/topology")
async def get_cytoscape_topology():
    """
    Returns network topology formatted for cytoscape.js / Graphology.
    Structure: { nodes: [...], edges: [...] }
    """
    try:
        devices = get_arp_table()
        
        # 1. Initialize cytoscape-compatible structure
        nodes = []
        edges = []

        # 2. Define the Central Hub (The Gateway)
        gateway_id = "gateway_01"
        nodes.append({
            "key": gateway_id,
            "attributes": {
                "label": "Network Gateway",
                "x": 0, "y": 0,           # cytoscape needs coordinates or a layout 
                "size": 15,
                "color": "#3b82f6",      # Blue
                "type": "router",
                "ip": "192.168.1.1"
            }
        })

        # 3. Add Discovered Hosts as Leaf Nodes
        for i, dev in enumerate(devices):
            node_key = f"node_{dev['mac'].replace(':', '')}"
            
            # Simple circular layout math so they don't all stack in the center
            import math
            angle = (i / len(devices)) * 2 * math.pi if devices else 0
            radius = 10
            
            nodes.append({
                "key": node_key,
                "attributes": {
                    "label": dev['ip'],
                    "x": radius * math.cos(angle),
                    "y": radius * math.sin(angle),
                    "size": 8,
                    "color": "#10b981",  # Green (Success/Online)
                    "mac": dev['mac'],
                    "interface": dev['interface'],
                    "type": "host"
                }
            })

            # 4. Create the Edge (Link)
            edges.append({
                "key": f"link_{node_key}",
                "source": gateway_id,
                "target": node_key,
                "attributes": {
                    "size": 2,
                    "color": "#cbd5e1"   # Light Gray
                }
            })

        return {
            "nodes": nodes,
            "edges": edges
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Topology Discovery Failed: {str(e)}")