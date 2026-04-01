def validate_parser_output(data: dict):
    if not isinstance(data, dict):
        raise ValueError("Invalid parser response format")

    # Required fields
    if "loops" not in data:
        raise ValueError("Parser missing 'loops' field")

    # Optional but expected
    if "fileType" not in data:
        data["fileType"] = "UNKNOWN"

    return data