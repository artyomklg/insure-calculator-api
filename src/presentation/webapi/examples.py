from typing import Any, Final

REQUEST_EXAMPLE: Final[dict[str, Any]] = {"2020-02-02": [{"cargo_type": "Default", "rate": 0.5}]}
RESPONSE_EXAMPLE: Final[dict[int | str, dict[str, Any]]] = {
    200: {
        "description": "Successful update",
        "content": {"application/json": {"example": REQUEST_EXAMPLE}},
    }
}
