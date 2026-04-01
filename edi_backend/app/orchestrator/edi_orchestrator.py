import time

from app.services.parser_client import call_parser_api
from app.services.validator_client import call_validator_api

from app.contracts.parser_contract import validate_parser_output
from app.contracts.validator_contract import validate_validator_output

from app.orchestrator.response_builder import error_response

# ⚔️ INTERNAL (Layer 2 helpers)
from app.services.internal.detector import detect_type
from app.services.internal.tree_builder import build_tree
from app.services.internal.risk_engine import calculate_risk

# ⚔️ PROCESSING (Layer 3 intelligence)
from app.services.processing.normalizer import normalize_parser_data
from app.services.processing.extractor import extract_data
from app.services.processing.validator_enhancer import enhance_validation
from app.services.processing.summary_builder import build_summary


# ⚔️ NEW — DEDUPLICATION
def deduplicate_errors(errors):
    seen = set()
    unique = []

    for err in errors:
        key = (err.get("segment_id"), err.get("message"))
        if key not in seen:
            seen.add(key)
            unique.append(err)

    return unique


def process_edi(text: str, file_id: str):
    start_time = time.time()

    try:
        # ⚔️ STEP 1 — PARSER
        try:
            parser_raw = call_parser_api(text)
        except Exception as e:
            print("🔥 PARSER CALL ERROR:", str(e))
            return error_response(f"Parser service failed: {str(e)}")

        # ⚔️ STEP 2 — PARSER CONTRACT
        try:
            parser_data = validate_parser_output(parser_raw)
        except Exception as e:
            print("🔥 PARSER CONTRACT ERROR:", str(e))
            return error_response(f"Invalid parser response: {str(e)}")

        # ⚔️ STEP 3 — NORMALIZATION
        parser_data = normalize_parser_data(parser_data)

        # ⚔️ STEP 4 — FILE TYPE DETECTION
        file_type = parser_data.get("fileType") or detect_type(text)

        # ⚔️ STEP 5 — EXTRACTION
        extracted = extract_data(parser_data)

        # ⚔️ STEP 6 — VALIDATOR
        validator_failed = False
        try:
            validator_raw = call_validator_api(parser_data)
            validator_data = validate_validator_output(validator_raw)
            errors = validator_data.get("errors", [])
        except Exception as e:
            print("⚠️ VALIDATOR FAILURE:", str(e))
            errors = []
            validator_failed = True

        # ⚔️ STEP 7 — ENHANCER
        extra_errors = enhance_validation(extracted)
        all_errors = errors + extra_errors

        # ⚔️ NEW — REMOVE DUPLICATES
        all_errors = deduplicate_errors(all_errors)

        # ⚔️ STEP 8 — SMART RISK
        if any(e.get("severity") == "HIGH" for e in all_errors):
            risk = "HIGH"
        else:
            risk = calculate_risk(len(all_errors))

        # ⚔️ STEP 9 — TREE
        tree = build_tree(parser_data.get("loops", []))

        # ⚔️ STEP 10 — SUMMARY
        summary = build_summary(parser_data, all_errors, extracted)

        # ⚔️ STEP 11 — RESPONSE
        processing_time = round(time.time() - start_time, 4)

        status = "success"
        if validator_failed:
            status = "success_with_warnings"

        return {
            "status": status,
            "data": {
                "fileType": file_type,
                "risk": risk,
                "summary": summary,
                "errors": all_errors,
                "tree": tree,
                "extracted": extracted
            },
            "meta": {
                "file_id": file_id,
                "processingTime": processing_time,
                "version": "v1"
            }
        }

    except ValueError as ve:
        print("🔥 VALUE ERROR:", str(ve))
        return error_response(str(ve))

    except Exception as e:
        print("🔥 ORCHESTRATOR CRASH:", str(e))
        return error_response(f"Processing failed: {str(e)}")