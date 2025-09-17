import logging
import sys
import uuid
from typing import Any, Dict

from fastapi import Request


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base: Dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            base["exc_info"] = self.formatException(record.exc_info)
        if hasattr(record, "request_id"):
            base["request_id"] = getattr(record, "request_id")
        return str(base)


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)


def get_request_id(request: Request) -> str:
    return request.headers.get("X-Request-ID", str(uuid.uuid4()))
