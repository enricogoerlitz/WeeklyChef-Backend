from typing import Union

UNEXPECTED_ERROR_RESULT = (
    {
        "msg": "An unexpected error has occored."
    }, 500
)


def bad_request(exp: Union[str, Exception]) -> tuple[dict, int]:
    return {"msg": str(exp)}, 400


def unauthorized(exp: Union[str, Exception]) -> tuple[dict, int]:
    return {"msg": str(exp)}, 401


def forbidden(exp: Union[str, Exception]) -> tuple[dict, int]:
    return {"msg": str(exp)}, 403


def not_found(exp: Union[str, Exception]) -> tuple[dict, int]:
    return {"msg": str(exp)}, 404


def conflict(exp: Union[str, Exception]) -> tuple[dict, int]:
    return {"msg": str(exp)}, 409


def server_error(exp: str | Exception) -> tuple[dict, int]:
    return {"msg": str(exp)}, 500
