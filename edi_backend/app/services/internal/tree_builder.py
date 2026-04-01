def build_tree(loops: list):
    if not isinstance(loops, list):
        return []

    return [
        {
            "segment": item.get("segment", "UNKNOWN"),
            "data": item
        }
        for item in loops
    ]