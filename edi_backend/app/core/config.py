import os


class Settings:
    def __init__(self):
        # ⚔️ STORAGE
        self.UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

        # ⚔️ FILE LIMITS
        self.MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 5))

        # ⚔️ EXTENSIONS
        raw_ext = os.getenv("ALLOWED_EXTENSIONS", ".edi,.txt,.dat")
        self.ALLOWED_EXTENSIONS = set(
            ext.strip().lower() for ext in raw_ext.split(",") if ext.strip()
        )

        # ⚔️ DEV MODE (CRITICAL CONTROL)
        self.DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"

        # ⚔️ SERVICE MODES
        self.PARSER_MODE = os.getenv("PARSER_MODE", "mock").lower()
        self.VALIDATOR_MODE = os.getenv("VALIDATOR_MODE", "mock").lower()

        # ⚔️ SERVICE URLS
        self.PARSER_URL = os.getenv("PARSER_URL", "http://localhost:9000/parse")
        self.VALIDATOR_URL = os.getenv("VALIDATOR_URL", "http://localhost:9001/validate")


settings = Settings()