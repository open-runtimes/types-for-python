from __future__ import annotations

from typing import Any

from open_runtimes.logger import Logger
from open_runtimes.request import RuntimeRequest
from open_runtimes.response import RuntimeResponse


class RuntimeContext:
    req: RuntimeRequest
    res: RuntimeResponse
    logger: Logger

    def __init__(self, logger: Logger) -> None:
        self.req = RuntimeRequest()
        self.res = RuntimeResponse()
        self.logger = logger

    def log(self, *messages: Any) -> None:
        self.logger.write(messages, Logger.TYPE_LOG)
        self.logger.write(['\n'], Logger.TYPE_LOG)

    def error(self, *messages: Any) -> None:
        self.logger.write(messages, Logger.TYPE_ERROR)
        self.logger.write(['\n'], Logger.TYPE_ERROR)
