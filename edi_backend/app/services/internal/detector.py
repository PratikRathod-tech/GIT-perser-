def detect_type(text: str) -> str:
    if "ST*837" in text:
        return "837"
    elif "ST*835" in text:
        return "835"
    elif "ST*834" in text:
        return "834"
    return "UNKNOWN"