def extract_data(parser_data: dict) -> dict:
    """
    Extract meaningful business data from normalized parser output.

    CURRENT SCOPE:
    - Extract basic claim information (CLM segments)
    - Safe against malformed data

    Returns:
    {
        "totalClaims": int,
        "claims": [
            {
                "claim_id": str,
                "amount": float
            }
        ]
    }
    """

    # ⚔️ FAIL-SAFE INPUT
    if not isinstance(parser_data, dict):
        return {
            "totalClaims": 0,
            "claims": []
        }

    loops = parser_data.get("loops", [])

    if not isinstance(loops, list):
        loops = []

    claims = []

    # ⚔️ CORE EXTRACTION LOOP
    for item in loops:
        if not isinstance(item, dict):
            continue

        segment = item.get("segment")

        # 🎯 CLAIM SEGMENT DETECTION
        if segment == "CLM":
            claim_id = item.get("claim_id") or item.get("CLM01") or "UNKNOWN"

            # amount handling (safe)
            raw_amount = item.get("amount") or item.get("CLM02") or 0

            try:
                amount = float(raw_amount)
            except (ValueError, TypeError):
                amount = 0

            claims.append({
                "claim_id": str(claim_id),
                "amount": amount
            })

    return {
        "totalClaims": len(claims),
        "claims": claims
    }