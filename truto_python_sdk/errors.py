import json

import aiohttp

# Error bodies are kept on the exception, so cap how much of one we read.
MAX_ERROR_BODY_BYTES = 64 * 1024


class TrutoApiError(aiohttp.ClientResponseError):
    """Raised when the Truto API responds with a 4xx or 5xx status.

    Subclasses ``aiohttp.ClientResponseError``, so existing ``except
    aiohttp.ClientResponseError`` handlers keep working, and ``.status``,
    ``.message``, ``.headers`` and ``.request_info`` are unchanged. On top of
    that it carries the response body Truto sent back:

    - ``body``: the raw response body as text (``None`` if it could not be read)
    - ``data``: the body parsed as JSON, or ``None`` if it isn't JSON
    """

    def __init__(
        self,
        request_info,
        history,
        *,
        status=None,
        message="",
        headers=None,
        body=None,
        data=None,
    ):
        # Defaults match aiohttp.ClientResponseError: copy/pickle rebuild the
        # error as ``cls(request_info, history)`` and then restore __dict__.
        super().__init__(request_info, history, status=status, message=message, headers=headers)
        self.body = body
        self.data = data

    @property
    def error(self):
        """Truto's error message (the ``error`` field of a JSON error body), if any."""
        if isinstance(self.data, dict):
            for key in ("error", "message"):
                value = self.data.get(key)
                if isinstance(value, str) and value:
                    return value
        return None

    @property
    def truto_error_insight(self):
        """Truto's ``truto_error_insight`` object from the error body, if any."""
        if isinstance(self.data, dict):
            return self.data.get("truto_error_insight")
        return None

    def __str__(self):
        base = super().__str__()
        detail = self.error
        if detail is None and self.body:
            detail = self.body[:500]
        return f"{base}, body={detail!r}" if detail else base


async def raise_for_status(response: aiohttp.ClientResponse):
    """Like ``response.raise_for_status()`` but reads the body first so the
    raised ``TrutoApiError`` carries Truto's error message."""
    if response.ok:
        return
    body = None
    data = None
    try:
        raw = await response.content.read(MAX_ERROR_BODY_BYTES)
        body = raw.decode(response.charset or "utf-8", errors="replace")
    except Exception:
        body = None
    if body:
        try:
            data = json.loads(body)
        except ValueError:
            data = None
    raise TrutoApiError(
        response.request_info,
        response.history,
        status=response.status,
        message=response.reason or "",
        headers=response.headers,
        body=body,
        data=data,
    )
