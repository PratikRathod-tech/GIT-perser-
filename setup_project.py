import os

BASE_DIR = "edi_backend"

STRUCTURE = {
    "app": {
        "api": {
            "routes": ["upload.py", "process.py", "chat.py"],
            "schemas": ["upload_schema.py", "process_schema.py", "chat_schema.py"],
            "dependencies": ["validators.py"],
        },
        "core": ["config.py", "constants.py", "logger.py"],
        "orchestrator": ["pipeline.py", "context.py", "contracts.py", "response_builder.py"],
        "services": [
            "parser_service.py",
            "detector_service.py",
            "extractor_service.py",
            "validator_service.py",
            "risk_engine.py",
            "tree_builder.py",
            "ai_service.py",
        ],
        "models": [
            "parser_models.py",
            "validator_models.py",
            "response_models.py",
            "common_models.py",
        ],
        "utils": ["file_handler.py", "encoding.py", "helpers.py"],
        "reliability": ["error_handler.py", "exceptions.py", "fallback.py"],
    },
    "uploads": {},
    "tests": {},
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)

        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for file_name in content:
                file_path = os.path.join(path, file_name)
                with open(file_path, "w") as f:
                    f.write("# Auto-generated file\n")

        else:
            os.makedirs(path, exist_ok=True)


def create_root_files():
    root_files = ["main.py", "requirements.txt", ".env", "README.md"]

    for file in root_files:
        file_path = os.path.join(BASE_DIR, file)
        with open(file_path, "w") as f:
            f.write("# Auto-generated file\n")


def add_init_files():
    for root, dirs, files in os.walk(BASE_DIR):
        if "__pycache__" in root:
            continue
        init_file = os.path.join(root, "__init__.py")
        with open(init_file, "w") as f:
            f.write("")


if __name__ == "__main__":
    os.makedirs(BASE_DIR, exist_ok=True)

    create_structure(BASE_DIR, STRUCTURE)
    create_root_files()
    add_init_files()

    print("Project structure created successfully.")