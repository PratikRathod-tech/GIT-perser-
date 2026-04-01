def success_response(data: dict, meta: dict = None):
    return {
        "status": "success",
        "data": data,
        "meta": meta or {}
    }


def error_response(message: str):
    return {
        "status": "failed",
        "message": message,
        "data": {},
        "meta": {}
    }