from typing import Any
from unittest.mock import Mock

from niquests import Response


def generate_requests_get_mock(json_response: Any, status_code: int | None = 200):
    def requests_get_mock(url: str, params: dict[str, Any] | None = None) -> Response:
        _ = url, params
        resp = Mock(spec=Response)
        resp.status_code = status_code
        resp.json.return_value = json_response
        return resp

    return requests_get_mock


def generate_requests_post_mock(json_response: Any, status_code: int | None = 200):
    def requests_get_mock(
        url: str,
        json: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Response:
        _ = url, json, payload
        resp = Mock(spec=Response)
        resp.status_code = status_code
        resp.json.return_value = json_response
        return resp

    return requests_get_mock
