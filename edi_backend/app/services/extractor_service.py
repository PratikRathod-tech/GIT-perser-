# Auto-generated file
def extract_data(parser_data: dict) -> dict:
    """
    Advanced EDI extractor.

    Extracts:
    - Claims (CLM segments)
    - Basic patient info (NM1 segments)
    - Provider info (NM1 segments)

    Always safe. Never crashes.
    """

    if not isinstance(parser_data, dict):
        return {
            "totalClaims": 0,
            "claims": [],
            "patients": [],
            "providers": []
        }

    loops = parser_data.get("loops", [])
    if not isinstance(loops, list):
        loops = []

    claims = []
    patients = []
    providers = []

    for item in loops:
        if not isinstance(item, dict):
            continue

        segment = item.get("segment", "").upper()

        # ⚔️ CLAIM EXTRACTION (CLM)
        if segment == "CLM":
            claim = {
                "claim_id": item.get("claim_id") or item.get("id") or "UNKNOWN",
                "amount": item.get("amount", 0),
                "status": item.get("status", "UNKNOWN")
            }
            claims.append(claim)

        # ⚔️ PATIENT EXTRACTION (NM1 with QC)
        elif segment == "NM1" and item.get("entity") == "PATIENT":
            patient = {
                "name": item.get("name", "UNKNOWN"),
                "id": item.get("id", "UNKNOWN")
            }
            patients.append(patient)

        # ⚔️ PROVIDER EXTRACTION (NM1 with 82 or 85)
        elif segment == "NM1" and item.get("entity") == "PROVIDER":
            provider = {
                "name": item.get("name", "UNKNOWN"),
                "id": item.get("id", "UNKNOWN")
            }
            providers.append(provider)

    return {
        "totalClaims": len(claims),
        "claims": claims,
        "patients": patients,
        "providers": providers
    }