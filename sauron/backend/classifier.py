def classify_event(parsed):
    """
    Maps parser output to Event model field names.
    Severity/signature logic is a placeholder — to be expanded later.
    """
    return {
        "timestamp": parsed.get("timestamp"),
        "source_ip": parsed.get("src_ip"),
        "dest_ip": parsed.get("dst_ip"),
        "protocol": parsed.get("proto"),
        "severity": "low",
        "signature": f"{parsed.get('proto', '')} {parsed.get('src_ip', '')} -> {parsed.get('dst_ip', '')}",
        "action": "LOGGED",
    }
