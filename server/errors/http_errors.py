""""""

UNEXPECTED_ERROR_RESULT = (
    {
        "msg": "An unexpected error has occored."
    }, 500
)


def bad_request(exp: Exception) -> tuple[dict, int]:
    return {"msg": str(exp)}, 400


def unauthorized(exp: Exception) -> tuple[dict, int]:
    return {"msg": str(exp)}, 401


def forbidden(exp: Exception) -> tuple[dict, int]:
    return {"msg": str(exp)}, 403


def not_found(exp: Exception) -> tuple[dict, int]:
    return {"msg": str(exp)}, 404


def conflict(exp: Exception) -> tuple[dict, int]:
    return {"msg": str(exp)}, 409
