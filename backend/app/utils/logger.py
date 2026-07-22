"""
AtherOS v1.0.0-rc1 — Structured Logging Framework

Features:
- StructuredFormatter: human-readable text OR JSON-line format
- RotatingFileHandler: size-based rotation (10 MB × 5 backups)
- JSON sink: separate machine-parseable log file
- Correlation ID injection from thread-local context
- Log level driven by ATHEROS settings
"""
from __future__ import annotations

import json
import logging
import logging.handlers
import os
import traceback
from pathlib import Path
from typing import Optional

from backend.app.utils.log_context import get_correlation_id, get_request_id

# ─── Paths ─────────────────────────────────────────────────────────────────────
_LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
_LOG_DIR.mkdir(parents=True, exist_ok=True)

_LOG_FILE = _LOG_DIR / "atheros.log"
_JSON_LOG_FILE = _LOG_DIR / "atheros.json.log"

_LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "DEBUG").upper()
_LOG_FORMAT = os.getenv("LOG_FORMAT", "text").lower()
_MAX_BYTES = int(os.getenv("LOG_MAX_SIZE_MB", "10")) * 1024 * 1024
_BACKUP_COUNT = int(os.getenv("LOG_MAX_BACKUPS", "5"))


# ─── Formatters ────────────────────────────────────────────────────────────────

class StructuredTextFormatter(logging.Formatter):
    """Human-readable log formatter with correlation IDs."""

    _LEVEL_COLORS = {
        "DEBUG":    "\033[36m",   # cyan
        "INFO":     "\033[32m",   # green
        "WARNING":  "\033[33m",   # yellow
        "ERROR":    "\033[31m",   # red
        "CRITICAL": "\033[35m",   # magenta
    }
    _RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        correlation_id = get_correlation_id() or "-"
        request_id = get_request_id() or "-"
        level = record.levelname
        color = self._LEVEL_COLORS.get(level, "")
        ts = self.formatTime(record, "%Y-%m-%dT%H:%M:%S")
        msg = record.getMessage()
        line = (
            f"{ts} {color}{level:8s}{self._RESET} "
            f"[corr={correlation_id} req={request_id}] "
            f"{record.name}:{record.lineno} — {msg}"
        )
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line


class JSONFormatter(logging.Formatter):
    """Machine-parseable JSON-line log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        from datetime import datetime, UTC
        payload: dict = {
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S") + f".{record.msecs:.0f}",
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "lineno": record.lineno,
            "message": record.getMessage(),
            "correlation_id": get_correlation_id() or None,
            "request_id": get_request_id() or None,
        }
        if record.exc_info:
            payload["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_tb(record.exc_info[2]),
            }
        return json.dumps(payload, default=str)


# ─── Logger factory ────────────────────────────────────────────────────────────

def _build_logger() -> logging.Logger:
    log = logging.getLogger("AtherOS")
    log.setLevel(getattr(logging, _LOG_LEVEL_STR, logging.DEBUG))
    log.handlers.clear()
    log.propagate = False

    # 1. Console handler (text format)
    console = logging.StreamHandler()
    console.setFormatter(StructuredTextFormatter())
    console.setLevel(getattr(logging, _LOG_LEVEL_STR, logging.DEBUG))
    log.addHandler(console)

    # 2. Rotating text file handler
    try:
        rot_file = logging.handlers.RotatingFileHandler(
            _LOG_FILE, maxBytes=_MAX_BYTES, backupCount=_BACKUP_COUNT, encoding="utf-8"
        )
        rot_file.setFormatter(StructuredTextFormatter())
        log.addHandler(rot_file)
    except OSError:
        pass  # Gracefully skip if filesystem unavailable

    # 3. JSON log file handler
    try:
        json_file = logging.handlers.RotatingFileHandler(
            _JSON_LOG_FILE, maxBytes=_MAX_BYTES, backupCount=_BACKUP_COUNT, encoding="utf-8"
        )
        json_file.setFormatter(JSONFormatter())
        log.addHandler(json_file)
    except OSError:
        pass

    return log


logger: logging.Logger = _build_logger()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a child logger namespaced under 'AtherOS.<name>'."""
    if name:
        return logger.getChild(name)
    return logger