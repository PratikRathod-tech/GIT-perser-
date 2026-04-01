import requests
import time
import os

# ⚔️ CONFIG
VALIDATOR_URL = os.getenv("VALIDATOR_URL", "http://localhost:9001/validate")
VALIDATOR_MODE = os.getenv("VALIDATOR_MODE", "mock").lower()  # mock | real


def _mock_validator(data: dict):
    print("⚠️ USING MOCK VALIDATOR")

    errors = []

    loops = data.get("loops", [])
    if not isinstance(loops, list):
        loops = []

    # ⚔️ RULE 1 — Missing CLM (no claims)
    has_claim = any(item.get("segment") == "CLM" for item in loops if isinstance(item, dict))
    if not has_claim:
        errors.append({
            "segment_id": "CLM",
            "message": "No claims found in file",
            "severity": "HIGH"
        })

    # ⚔️ RULE 2 — Invalid claim data
    for item in loops:
        if not isinstance(item, dict):
            continue

        if item.get("segment") == "CLM":
            claim_id = item.get("claim_id")
            amount = item.get("amount")

            if not claim_id:
                errors.append({
                    "segment_id": "CLM",
                    "message": "Missing claim_id",
                    "severity": "HIGH"
                })

            if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
                errors.append({
                    "segment_id": "CLM",
                    "message": f"Invalid claim amount: {amount}",
                    "severity": "MEDIUM"
                })

    # ⚔️ RULE 3 — Missing Patient
    has_patient = any(
        item.get("segment") == "NM1" and item.get("entity") == "PATIENT"
        for item in loops if isinstance(item, dict)
    )
    if not has_patient:
        errors.append({
            "segment_id": "NM1",
            "message": "Missing patient information",
            "severity": "HIGH"
        })

    # ⚔️ RULE 4 — Missing Provider
    has_provider = any(
        item.get("segment") == "NM1" and item.get("entity") == "PROVIDER"
        for item in loops if isinstance(item, dict)
    )
    if not has_provider:
        errors.append({
            "segment_id": "NM1",
            "message": "Missing provider information",
            "severity": "MEDIUM"
        })

    return {
        "errors": errors
    }


def _validate_validator_response(data):
    if not isinstance(data, dict):
        raise ValueError("Validator response must be a dictionary")

    if "errors" not in data:
        raise ValueError("Validator response missing 'errors'")

    if not isinstance(data["errors"], list):
        raise ValueError("'errors' must be a list")

    normalized_errors = []
    for err in data["errors"]:
        if not isinstance(err, dict):
            continue

        normalized_errors.append({
            "segment_id": err.get("segment_id", "UNKNOWN"),
            "message": err.get("message", "Unknown error"),
            "severity": err.get("severity", "LOW")
        })

    data["errors"] = normalized_errors
    return data


def call_validator_api(data: dict, retries: int = 2):

    # ⚔️ INPUT SAFETY
    if not isinstance(data, dict):
        raise ValueError("Invalid input for validator")

    # ⚔️ MOCK MODE
    if VALIDATOR_MODE == "mock":
        return _validate_validator_response(_mock_validator(data))

    # ⚔️ REAL MODE
    print("⚔️ USING REAL VALIDATOR")

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                VALIDATOR_URL,
                json=data,
                timeout=3
            )

            response.raise_for_status()

            result = response.json()

            return _validate_validator_response(result)

        except requests.exceptions.Timeout:
            print(f"⚠️ Validator timeout (attempt {attempt + 1})")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Validator request failed (attempt {attempt + 1}):", str(e))

        except ValueError as ve:
            print(f"⚠️ Validator invalid response:", str(ve))
            raise

        if attempt == retries:
            raise ValueError("Validator service failed after retries")

        time.sleep(1)