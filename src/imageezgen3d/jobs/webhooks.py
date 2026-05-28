from __future__ import annotations

import json
from typing import Any
from urllib import error, request


def deliver_webhook(
    url: str,
    payload: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
) -> tuple[bool, str | None]:
    """POST JSON completion payload; returns (delivered, error_message)."""
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            if 200 <= response.status < 300:
                return True, None
            return False, f"Unexpected webhook status: {response.status}"
    except error.URLError as exc:
        return False, str(exc.reason if hasattr(exc, "reason") else exc)
