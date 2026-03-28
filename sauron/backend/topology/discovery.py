import os

def get_arp_table():
    """
    Parses the /proc/net/arp file and returns a list of dictionaries.
    Each dictionary represents a discovered device on the local segment.
    """
    arp_table = []
    arp_path = "/proc/net/arp"

    if not os.path.exists(arp_path):
        # Fallback for non-Linux environments
        return [{"ip": "127.0.0.1", "mac": "00:00:00:00:00:00", "interface": "lo", "status": "local"}]

    try:
        with open(arp_path, "r") as f:
            # Skip the header line: 
            # IP address       HW type     Flags       HW address            Mask     Device
            lines = f.readlines()[1:]
            
            for line in lines:
                parts = line.split()
                if len(parts) < 6:
                    continue

                ip_address = parts[0]
                hw_type    = parts[1]
                flags      = parts[2]
                hw_address = parts[3]
                device     = parts[5]

                # Ignore incomplete entries (MAC is all zeros)
                if hw_address == "00:00:00:00:00:00":
                    continue

                arp_table.append({
                    "ip": ip_address,
                    "mac": hw_address,
                    "interface": device,
                    # Flag 0x2 is 'Complete', 0x6 is 'Permanent/Static'
                    "is_static": flags == "0x6",
                    "status": "online"
                })
    except Exception as e:
        print(f"Error reading ARP table: {e}")
        
    return arp_table

def generate_topology_data():
    """
    Formats the ARP table into a Cytoscape-ready 'nodes and edges' structure.
    """
    devices = get_arp_table()
    
    # Define your local Gateway (usually .1)
    nodes = [{ "data": { "id": "gateway", "label": "Gateway", "type": "router" } }]
    edges = []

    for i, dev in enumerate(devices):
        node_id = f"node_{i}"
        nodes.append({
            "data": {
                "id": node_id,
                "label": dev["ip"],
                "mac": dev["mac"],
                "type": "host",
                "status": dev["status"]
            }
        })
        # In a basic flat network, everyone connects to the Gateway
        edges.append({
            "data": {
                "id": f"edge_{i}",
                "source": "gateway",
                "target": node_id
            }
        })

    return {"nodes": nodes, "edges": edges}
"""
if __name__ == "__main__":
    # Test the output
    import pprint
    pprint.pprint(generate_topology_data())
"""