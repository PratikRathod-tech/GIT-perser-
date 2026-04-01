def validate_validator_output(data: dict):
    if not isinstance(data, dict):
        raise ValueError("Invalid validator response")

    if "errors" not in data:
        raise ValueError("Validator missing 'errors' field")

    return data