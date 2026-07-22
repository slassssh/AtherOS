"""
AtherOS — Log Context Management

Provides thread-local storage for correlation_id and request_id.
These are injected automatically into all log records via the log formatters.

Usage:
    with LogContext(correlation_id="abc-123", request_id="req-456"):
        logger.info("This log carries both IDs automatically")

    # Or imperatively:
    set_correlation_id("my-corr-id")
    logger.info("Correlated log")
"""
from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Generator, Optional
from uuid import uuid4

_local = threading.local()


def set_correlation_id(value: str) -> None:
    """Set the correlation ID for the current thread."""
    _local.correlation_id = value


def get_correlation_id() -> Optional[str]:
    """Get the correlation ID for the current thread, or None."""
    return getattr(_local, "correlation_id", None)


def clear_correlation_id() -> None:
    """Clear the correlation ID for the current thread."""
    _local.correlation_id = None


def set_request_id(value: str) -> None:
    """Set the request ID for the current thread."""
    _local.request_id = value


def get_request_id() -> Optional[str]:
    """Get the request ID for the current thread, or None."""
    return getattr(_local, "request_id", None)


def clear_request_id() -> None:
    """Clear the request ID for the current thread."""
    _local.request_id = None


@contextmanager
def LogContext(
    correlation_id: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Context manager that sets and clears correlation/request IDs for the current thread.
    Auto-generates a correlation_id UUID if none is provided.

    Yields the active correlation_id.
    """
    corr = correlation_id or str(uuid4())
    req = request_id or corr

    prev_corr = get_correlation_id()
    prev_req = get_request_id()

    set_correlation_id(corr)
    set_request_id(req)
    try:
        yield corr
    finally:
        # Restore previous values (support nested contexts)
        if prev_corr is not None:
            set_correlation_id(prev_corr)
        else:
            clear_correlation_id()

        if prev_req is not None:
            set_request_id(prev_req)
        else:
            clear_request_id()


def new_correlation_id() -> str:
    """Generate and set a fresh UUID4 correlation ID. Returns it."""
    cid = str(uuid4())
    set_correlation_id(cid)
    return cid
