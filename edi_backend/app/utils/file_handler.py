# Auto-generated file
import os
import uuid
from app.core.config import settings

def generate_file_id():
    return str(uuid.uuid4())

def get_file_path(file_id: str):
    return os.path.join(settings.UPLOAD_DIR, f"{file_id}.edi")

def save_file(content: str, file_id: str):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = get_file_path(file_id)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path