from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime
from io import StringIO
from typing import Any, List, Optional, Sequence


class Logger:
    TYPE_ERROR: str = 'error'
    TYPE_LOG: str = 'log'

    id: str
    enabled: bool
    includes_native_info: bool

    stream_logs: Any
    stream_errors: Any
    custom_std: Optional[StringIO]

    def __init__(self, status: Optional[str] = None, id: Optional[str] = None) -> None:
        self.id = ''
        self.enabled = False
        self.includes_native_info = False
        self.stream_logs = None
        self.stream_errors = None
        self.custom_std = None

        if status is None or status == '':
            self.enabled = True
        else:
            self.enabled = status == 'enabled'

        if self.enabled:
            is_development = os.getenv('OPEN_RUNTIMES_ENV') == 'development'

            if id is None or id == '':
                if is_development:
                    self.id = 'dev'
                else:
                    self.id = self.generate_id()
            else:
                self.id = id

            self.stream_logs = open('/mnt/logs/' + self.id + '_logs.log', 'a')
            self.stream_errors = open('/mnt/logs/' + self.id + '_errors.log', 'a')

    def write(
        self,
        messages: Sequence[Any],
        type: Optional[str] = None,
        is_native: bool = False,
    ) -> None:
        if type is None:
            type = Logger.TYPE_LOG

        if not self.enabled:
            return

        if is_native and not self.includes_native_info:
            self.includes_native_info = True
            self.write(
                ['Native logs detected. Use context.log() or context.error() for better experience.']
            )

        stream = self.stream_logs
        if type == Logger.TYPE_ERROR:
            stream = self.stream_errors

        string_log = ''
        i = 0
        for message in messages:
            if isinstance(message, (list, dict, tuple)):
                string_log += json.dumps(message, separators=(',', ':'))
            else:
                string_log += str(message)

            if i < len(messages) - 1:
                string_log += ' '
            i += 1

        if len(string_log) > 8000:
            string_log = string_log[:8000]
            string_log += '... Log truncated due to size limit (8000 characters)'

        try:
            stream.write(string_log)
        except Exception:
            pass

    def end(self) -> None:
        if not self.enabled:
            return

        self.enabled = False

        self.stream_logs.close()
        self.stream_errors.close()

    def override_native_logs(self) -> None:
        sys.stderr = sys.stdout = self.custom_std = StringIO()

    def revert_native_logs(self) -> None:
        if self.custom_std is not None and self.custom_std.getvalue():
            self.write([self.custom_std.getvalue()], Logger.TYPE_LOG, True)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def generate_id(self, padding: int = 7) -> str:
        now = datetime.now()
        sec = int(now.timestamp())
        usec = now.microsecond % 1000
        base_id = f'{sec:08x}{usec:05x}'
        random_bytes = os.urandom(math.ceil(padding / 2))
        random_padding = random_bytes.hex()[:padding]
        return base_id + random_padding
