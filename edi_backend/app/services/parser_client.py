import requests
import time
import os

# ⚔️ CONFIG
PARSER_URL = os.getenv("PARSER_URL", "http://localhost:9000/parse")
PARSER_MODE = os.getenv("PARSER_MODE", "mock").lower()  # mock | real


def _mock_parser(text: str):
    print("⚠️ USING MOCK PARSER")

    text = text.strip().lower()

    # ⚔️ CASE 1 — BAD DATA
    if text == "bad":
        return {
            "fileType": "837",
            "loops": [
                {"segment": "ISA"},
                {"segment": "CLM", "claim_id": "", "amount": -500},
                {"segment": "NM1", "entity": "PROVIDER", "name": "", "id": None}
            ]
        }

    # ⚔️ CASE 2 — MISSING FIELDS
    if text == "missing":
        return {
            "fileType": "837",
            "loops": [
                {"segment": "ISA"},
                {"segment": "CLM", "amount": None},
                {"segment": "NM1", "entity": "PATIENT"}
            ]
        }

    # ⚔️ CASE 3 — EMPTY FILE
    if text == "empty":
        return {
            "fileType": "837",
            "loops": []
        }

    # ⚔️ DEFAULT — NORMAL DATA
    return {
        "fileType": "837",
        "loops": [
            {"segment": "ISA"},
            {"segment": "GS"},
            {"segment": "ST"},

            {"segment": "NM1", "entity": "PATIENT", "name": "John Doe", "id": "P001"},
            {"segment": "NM1", "entity": "PROVIDER", "name": "Dr Smith", "id": "PR001"},

            {"segment": "CLM", "claim_id": "C123", "amount": 500, "status": "ACTIVE"},
            {"segment": "CLM", "claim_id": "C456", "amount": 1200, "status": "PENDING"}
        ]
    }


def _validate_parser_response(data):
    if not isinstance(data, dict):
        raise ValueError("Parser response must be a dictionary")

    if "loops" not in data:
        raise ValueError("Parser response missing 'loops'")

    if not isinstance(data["loops"], list):
        raise ValueError("'loops' must be a list")

    if "fileType" not in data:
        data["fileType"] = "UNKNOWN"

    # ⚔️ sanitize loops
    clean_loops = []
    for item in data["loops"]:
        if isinstance(item, dict) and "segment" in item:
            clean_loops.append(item)

    data["loops"] = clean_loops

    return data


def call_parser_api(text: str, retries: int = 2):

    # ⚔️ INPUT SAFETY
    if not text or not isinstance(text, str):
        raise ValueError("Invalid input text for parser")

    # ⚔️ MOCK MODE
    if PARSER_MODE == "mock":
        return _validate_parser_response(_mock_parser(text))

    # ⚔️ REAL MODE
    print("⚔️ USING REAL PARSER")

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                PARSER_URL,
                json={"text": text},
                timeout=3
            )

            response.raise_for_status()

            data = response.json()

            return _validate_parser_response(data)

        except requests.exceptions.Timeout:
            print(f"⚠️ Parser timeout (attempt {attempt + 1})")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Parser request failed (attempt {attempt + 1}):", str(e))

        except ValueError as ve:
            print(f"⚠️ Parser invalid response:", str(ve))
            raise

        if attempt == retries:
            raise ValueError("Parser service failed after retries")

        time.sleep(1)