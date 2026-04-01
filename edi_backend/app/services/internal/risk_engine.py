def calculate_risk(error_count: int) -> str:
    if error_count > 5:
        return "HIGH"
    elif error_count > 2:
        return "MEDIUM"
    return "LOW"