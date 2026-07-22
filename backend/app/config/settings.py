"""
AtherOS v1.0.0-rc1 — Centralized Settings
Supports: environment variables, .env file, runtime overrides, multi-profile.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv

load_dotenv()

_ENV = os.getenv("ATHEROS_ENV", os.getenv("ENVIRONMENT", "development")).lower()


class Settings:
    """
    Production-grade AtherOS Settings.
    Resolution priority (highest → lowest):
      runtime override > environment variable > .env file > profile default
    """

    # ─── Identity ──────────────────────────────────────────────────────
    app_name: str
    version: str
    environment: Literal["development", "testing", "production"]
    debug: bool

    # ─── API ───────────────────────────────────────────────────────────
    api_host: str
    api_port: int
    api_workers: int
    secret_key: str
    cors_origins: str

    # ─── Database ──────────────────────────────────────────────────────
    database_url: str
    db_pool_size: int
    db_echo: bool

    # ─── LLM ───────────────────────────────────────────────────────────
    llm_provider: str
    llm_api_key: str
    llm_model_name: str
    llm_base_url: str
    llm_timeout_seconds: int
    llm_max_retries: int

    # ─── Workspace / Filesystem ────────────────────────────────────────
    workspace_root: str
    backup_dir: str

    # ─── Logging ───────────────────────────────────────────────────────
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    log_format: Literal["text", "json"]
    log_dir: str
    log_max_size_mb: int
    log_max_backups: int

    # ─── Health / Observability ────────────────────────────────────────
    health_check_interval_seconds: int
    benchmark_iterations: int

    # ─── Cluster ───────────────────────────────────────────────────────
    cluster_enabled: bool
    cluster_node_id: str
    cluster_heartbeat_timeout_seconds: int

    # ─── Plugin ────────────────────────────────────────────────────────
    plugin_dir: str
    plugin_auto_discover: bool

    def __init__(self, overrides: Optional[dict] = None) -> None:
        overrides = overrides or {}

        def _get(key: str, default: object) -> object:
            if key in overrides:
                return overrides[key]
            return os.getenv(key, default)  # type: ignore[arg-type]

        def _bool(key: str, default: bool) -> bool:
            val = _get(key, str(default))
            return str(val).lower() in ("1", "true", "yes")

        def _int(key: str, default: int) -> int:
            return int(_get(key, default))  # type: ignore[arg-type]

        # Detect profile defaults
        p = _ProfileDefaults.for_env(_ENV)

        self.app_name = str(_get("APP_NAME", "AtherOS"))
        self.version = str(_get("APP_VERSION", "1.0.0-rc1"))
        self.environment = str(_get("ATHEROS_ENV", _ENV))  # type: ignore[assignment]
        self.debug = _bool("DEBUG", p.debug)

        self.api_host = str(_get("API_HOST", "0.0.0.0"))
        self.api_port = _int("API_PORT", 8000)
        self.api_workers = _int("API_WORKERS", p.api_workers)
        self.secret_key = str(_get("SECRET_KEY", "atheros_default_secret_key_change_in_prod"))
        self.cors_origins = str(_get("CORS_ORIGINS", "*"))

        self.database_url = str(_get("DATABASE_URL", "sqlite:///./atheros.db"))
        self.db_pool_size = _int("DB_POOL_SIZE", p.db_pool_size)
        self.db_echo = _bool("DB_ECHO", p.db_echo)

        self.llm_provider = str(_get("LLM_PROVIDER", "mock"))
        self.llm_api_key = str(_get("LLM_API_KEY", ""))
        self.llm_model_name = str(_get("LLM_MODEL_NAME", "gpt-4o-mini"))
        self.llm_base_url = str(_get("LLM_BASE_URL", ""))
        self.llm_timeout_seconds = _int("LLM_TIMEOUT_SECONDS", 60)
        self.llm_max_retries = _int("LLM_MAX_RETRIES", 3)

        self.workspace_root = str(_get("WORKSPACE_ROOT", str(Path.cwd())))
        self.backup_dir = str(_get("BACKUP_DIR", str(Path.cwd() / "backups")))

        self.log_level = str(_get("LOG_LEVEL", p.log_level))  # type: ignore[assignment]
        self.log_format = str(_get("LOG_FORMAT", p.log_format))  # type: ignore[assignment]
        self.log_dir = str(_get("LOG_DIR", "logs"))
        self.log_max_size_mb = _int("LOG_MAX_SIZE_MB", 10)
        self.log_max_backups = _int("LOG_MAX_BACKUPS", 5)

        self.health_check_interval_seconds = _int("HEALTH_CHECK_INTERVAL_SECONDS", 30)
        self.benchmark_iterations = _int("BENCHMARK_ITERATIONS", 10)

        self.cluster_enabled = _bool("CLUSTER_ENABLED", False)
        self.cluster_node_id = str(_get("CLUSTER_NODE_ID", "node-local-01"))
        self.cluster_heartbeat_timeout_seconds = _int("CLUSTER_HEARTBEAT_TIMEOUT_SECONDS", 10)

        self.plugin_dir = str(_get("PLUGIN_DIR", "plugins"))
        self.plugin_auto_discover = _bool("PLUGIN_AUTO_DISCOVER", True)

    def validate(self) -> None:
        """Validates required constraints. Raises ValueError on violations."""
        if not self.app_name:
            raise ValueError("APP_NAME cannot be empty")

        valid_envs = ("development", "testing", "production")
        if self.environment not in valid_envs:
            raise ValueError(f"ATHEROS_ENV must be one of {valid_envs}, got '{self.environment}'")

        valid_log_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        if self.log_level not in valid_log_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_log_levels}")

        if self.environment == "production":
            if self.secret_key == "atheros_default_secret_key_change_in_prod":
                raise ValueError("SECRET_KEY must be overridden in production")
            if self.debug:
                raise ValueError("DEBUG must be False in production")

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __repr__(self) -> str:
        return f"<Settings env={self.environment} version={self.version} debug={self.debug}>"


class _ProfileDefaults:
    """Internal per-environment default values."""

    def __init__(
        self,
        debug: bool,
        log_level: str,
        log_format: str,
        api_workers: int,
        db_pool_size: int,
        db_echo: bool,
    ) -> None:
        self.debug = debug
        self.log_level = log_level
        self.log_format = log_format
        self.api_workers = api_workers
        self.db_pool_size = db_pool_size
        self.db_echo = db_echo

    @classmethod
    def for_env(cls, env: str) -> "_ProfileDefaults":
        if env == "production":
            return cls(
                debug=False,
                log_level="INFO",
                log_format="json",
                api_workers=4,
                db_pool_size=10,
                db_echo=False,
            )
        if env == "testing":
            return cls(
                debug=True,
                log_level="WARNING",
                log_format="text",
                api_workers=1,
                db_pool_size=1,
                db_echo=False,
            )
        # development (default)
        return cls(
            debug=True,
            log_level="DEBUG",
            log_format="text",
            api_workers=1,
            db_pool_size=5,
            db_echo=False,
        )