from typing import Any, Dict, Optional
from unittest.mock import Mock

from requests import Response


def generate_requests_get_mock(json_response: Any, status_code: Optional[int] = 200):
    def requests_get_mock(url: str, params: Optional[Dict[str, Any]] = {}) -> Response:
        _ = url, params
        resp = Mock(spec=Response)
        resp.status_code = status_code
        resp.json.return_value = json_response
        return resp

    return requests_get_mock
