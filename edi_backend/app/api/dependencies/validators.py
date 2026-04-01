from fastapi import UploadFile, HTTPException
import os
from app.core.config import settings


def validate_file(file: UploadFile):
    rules = [
        check_file_exists,
        check_file_extension,
        check_file_size,
    ]

    for rule in rules:
        rule(file)


def check_file_exists(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")


def check_file_extension(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")


def check_file_size(file: UploadFile):
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")


def check_edi_structure(text: str):
    """
    EDI structure validation with DEV MODE support
    """

    if not text:
        raise ValueError("Empty content")

    # ⚔️ DEV MODE: Skip strict validation
    if getattr(settings, "DEV_MODE", False):
        print("⚠️ DEV MODE: Skipping strict EDI validation")
        return True

    # ⚔️ STRICT MODE (PRODUCTION)
    required_segments = ["ISA", "GS", "ST"]

    found = any(segment in text for segment in required_segments)

    if not found:
        raise ValueError("Invalid EDI structure: missing required segments")

    return True