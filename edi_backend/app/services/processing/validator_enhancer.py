def enhance_validation(extracted: dict) -> list:
    """
    Add lightweight validation on top of external validator output.

    This is NOT a replacement for validator service.
    It only performs:
    - sanity checks
    - missing field checks
    - basic domain validation

    Input:
        extracted (dict)

    Output:
        List of error dictionaries
    """

    # ⚔️ FAIL-SAFE INPUT
    if not isinstance(extracted, dict):
        return []

    claims = extracted.get("claims", [])

    if not isinstance(claims, list):
        claims = []

    errors = []

    for claim in claims:
        if not isinstance(claim, dict):
            continue

        claim_id = claim.get("claim_id")
        amount = claim.get("amount")

        # ⚔️ CHECK 1 — Missing claim ID
        if not claim_id or claim_id == "UNKNOWN":
            errors.append({
                "error_id": "VAL_ENH_001",
                "segment_id": "CLM",
                "message": "Missing claim ID",
                "severity": "MEDIUM"
            })

        # ⚔️ CHECK 2 — Invalid amount type
        if not isinstance(amount, (int, float)):
            errors.append({
                "error_id": "VAL_ENH_002",
                "segment_id": "CLM",
                "message": "Invalid amount format",
                "severity": "HIGH"
            })
            continue

        # ⚔️ CHECK 3 — Negative amount
        if amount < 0:
            errors.append({
                "error_id": "VAL_ENH_003",
                "segment_id": "CLM",
                "message": "Negative claim amount",
                "severity": "HIGH"
            })

        # ⚔️ CHECK 4 — Zero amount (warning level)
        if amount == 0:
            errors.append({
                "error_id": "VAL_ENH_004",
                "segment_id": "CLM",
                "message": "Zero claim amount",
                "severity": "LOW"
            })

    return errors