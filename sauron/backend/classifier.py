def classify_event(parsed):
    """
    Maps parser output to Event model field names.
    Severity/signature logic is a placeholder — to be expanded later.
    """
    return {
        "timestamp": parsed.get("timestamp"),
        "src_ip": parsed.get("src_ip"),
        "dst_ip": parsed.get("dst_ip"),
        "protocol": parsed.get("proto"),
        "severity": "low",
        "description": f"{parsed.get('proto', '')} {parsed.get('src_ip', '')} -> {parsed.get('dst_ip', '')}",
        "action": "LOGGED",
    }
