import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.api.dependencies.validators import validate_file, check_edi_structure
from app.utils.file_handler import generate_file_id, save_file
from app.utils.encoding import normalize_text
from app.orchestrator.response_builder import error_response

# ⚔️ NEW — Layer 2 Orchestrator
from app.orchestrator.edi_orchestrator import process_edi

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    start_time = time.time()

    try:
        # ⚔️ STEP 1: File-level validation
        validate_file(file)

        # ⚔️ STEP 2: Read file
        raw_bytes = await file.read()
        if not raw_bytes:
            raise ValueError("File is empty")

        # ⚔️ STEP 3: Normalize (binary → text)
        normalized_text = normalize_text(raw_bytes)

        # ⚔️ STEP 4: Content validation
        check_edi_structure(normalized_text)

        # ⚔️ STEP 5: Generate ID
        file_id = generate_file_id()

        # ⚔️ STEP 6: Store file
        save_file(normalized_text, file_id)

        # ⚔️ STEP 7: HANDOVER TO LAYER 2 (IMPORTANT)
        result = process_edi(normalized_text, file_id)

        return JSONResponse(content=result)

    # ⚔️ USER ERROR — FastAPI validation (extension, size)
    except HTTPException as he:
        print("DEBUG HTTPException:", he.detail)
        return JSONResponse(
            status_code=he.status_code,
            content=error_response(he.detail)
        )

    # ⚔️ USER ERROR — our validation (empty, invalid content)
    except ValueError as ve:
        print("DEBUG ValueError:", str(ve))
        return JSONResponse(
            status_code=400,
            content=error_response(str(ve))
        )

    # ⚔️ SYSTEM ERROR — unexpected
    except Exception as e:
        print("DEBUG UNKNOWN ERROR:", str(e))
        return JSONResponse(
            status_code=500,
            content=error_response("Unexpected system error")
        )