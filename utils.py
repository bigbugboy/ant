from typing import Any, Dict


def response_success(data: Any, msg: str = "") -> Dict[str, Any]:
    return {"data": data, "msg": msg, "status": "success"}


def response_error(error_msg: str = "") -> Dict[str, str]:
    return {"status": "error", "msg": error_msg}