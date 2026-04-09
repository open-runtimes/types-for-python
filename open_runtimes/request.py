from __future__ import annotations

import json
from typing import Any, Dict, List, Union


class RuntimeRequest:
    body_binary: bytes
    headers: Dict[str, str]
    method: str
    url: str
    path: str
    port: int
    query: Dict[str, str]
    query_string: str
    scheme: str
    host: str

    def __init__(
        self,
        body_binary: bytes = b'',
        headers: Union[Dict[str, str], None] = None,
        method: str = '',
        url: str = '',
        path: str = '',
        port: int = 80,
        query: Union[Dict[str, str], None] = None,
        query_string: str = '',
        scheme: str = '',
        host: str = '',
    ) -> None:
        self.body_binary = body_binary
        self.headers = headers if headers is not None else {}
        self.method = method
        self.url = url
        self.path = path
        self.port = port
        self.query = query if query is not None else {}
        self.query_string = query_string
        self.scheme = scheme
        self.host = host

    @property
    def body_text(self) -> str:
        return self.body_binary.decode('utf-8')

    @property
    def body_json(self) -> Any:
        return json.loads(self.body_text)

    @property
    def body_raw(self) -> str:
        return self.body_text

    @property
    def body(self) -> Any:
        content_type = self.headers.get('content-type', 'text/plain').lower()

        if content_type.startswith('application/json'):
            if len(self.body_binary) > 0:
                return self.body_json
            else:
                return {}

        return self.body_text
