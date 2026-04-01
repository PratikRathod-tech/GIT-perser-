def normalize_text(raw_bytes: bytes) -> str:
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Invalid encoding: must be UTF-8")

    # Normalize whitespace
    text = text.replace("\r\n", "\n").strip()

    if not text:
        raise ValueError("Empty file after normalization")

    return text