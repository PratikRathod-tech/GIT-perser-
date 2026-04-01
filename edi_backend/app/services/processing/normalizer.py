def normalize_parser_data(data: dict) -> dict:
    """
    Normalize parser output into a safe, predictable structure.

    Guarantees:
    - Always returns a dict
    - Always has 'fileType' (string)
    - Always has 'loops' (list of dicts)
    """

    # ⚔️ HARD FAIL-SAFE: invalid input
    if not isinstance(data, dict):
        return {
            "fileType": "UNKNOWN",
            "loops": []
        }

    # ⚔️ FILE TYPE NORMALIZATION
    file_type = data.get("fileType")
    if not isinstance(file_type, str) or not file_type.strip():
        file_type = "UNKNOWN"

    # ⚔️ LOOPS NORMALIZATION
    raw_loops = data.get("loops")

    if not isinstance(raw_loops, list):
        raw_loops = []

    normalized_loops = []

    for item in raw_loops:
        # skip invalid entries
        if not isinstance(item, dict):
            continue

        segment = item.get("segment")
        if not isinstance(segment, str) or not segment.strip():
            segment = "UNKNOWN"

        # keep full data but ensure structure
        normalized_loops.append({
            "segment": segment,
            **item  # preserve all original fields
        })

    return {
        "fileType": file_type,
        "loops": normalized_loops
    }