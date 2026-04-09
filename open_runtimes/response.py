from __future__ import annotations

import json
from typing import Any, Dict, Optional, Union


class RuntimeOutput:
    body: bytes
    status_code: int
    headers: Dict[str, str]

    def __init__(
        self,
        body: bytes,
        status_code: int,
        headers: Dict[str, str],
    ) -> None:
        self.body = body
        self.status_code = status_code
        self.headers = headers


class RuntimeResponse:
    def binary(
        self,
        bytes_data: bytes,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ) -> RuntimeOutput:
        return RuntimeOutput(bytes_data, status_code, headers if headers is not None else {})

    def text(
        self,
        body: str,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ) -> RuntimeOutput:
        return self.binary(body.encode('utf-8'), status_code, headers)

    def send(
        self,
        body: str,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ) -> RuntimeOutput:
        return self.text(body, status_code, headers)

    def json(
        self,
        obj: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ) -> RuntimeOutput:
        if headers is None:
            headers = {}
        headers['content-type'] = 'application/json'
        return self.text(json.dumps(obj, separators=(',', ':')), status_code, headers)

    def empty(self) -> RuntimeOutput:
        return self.text('', 204, {})

    def redirect(
        self,
        url: str,
        status_code: int = 301,
        headers: Optional[Dict[str, str]] = None,
    ) -> RuntimeOutput:
        if headers is None:
            headers = {}
        headers['location'] = url
        return self.text('', status_code, headers)
