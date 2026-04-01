def build_summary(parser_data: dict, errors: list, extracted: dict) -> dict:
    """
    Build a human-readable summary of the EDI file.

    Combines:
    - structural info (segments)
    - validation info (errors)
    - extracted business data (claims)

    Input:
        parser_data (dict)
        errors (list)
        extracted (dict)

    Output:
        {
            "totalSegments": int,
            "errorsCount": int,
            "totalClaims": int,
            "hasErrors": bool
        }
    """

    # ⚔️ SAFE INPUT HANDLING
    if not isinstance(parser_data, dict):
        parser_data = {}

    if not isinstance(errors, list):
        errors = []

    if not isinstance(extracted, dict):
        extracted = {}

    loops = parser_data.get("loops", [])
    if not isinstance(loops, list):
        loops = []

    total_segments = len(loops)
    error_count = len(errors)
    total_claims = extracted.get("totalClaims", 0)

    if not isinstance(total_claims, int):
        total_claims = 0

    return {
        "totalSegments": total_segments,
        "errorsCount": error_count,
        "totalClaims": total_claims,
        "hasErrors": error_count > 0
    }