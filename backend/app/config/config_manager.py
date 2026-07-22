"""
AtherOS ConfigManager — Centralized configuration with YAML overlay and runtime overrides.
Resolution priority: runtime override > environment variable > .env > config.yaml > profile default
"""
from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, Optional

from backend.app.config.settings import Settings

try:
    import yaml  # type: ignore[import-untyped]
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


_CONFIG_YAML_PATH = Path("config.yaml")


class ConfigManager:
    """
    Singleton configuration manager for AtherOS.

    Layers (highest → lowest priority):
      1. Runtime overrides (set_override / clear_override)
      2. Environment variables / .env file
      3. config.yaml (if present)
      4. Profile defaults (dev / test / prod)
    """

    _instance: Optional["ConfigManager"] = None
    _settings: Optional[Settings] = None
    _yaml_data: Dict[str, Any] = {}
    _overrides: Dict[str, Any] = {}
    _initialized_at: Optional[datetime] = None

    def __new__(cls) -> "ConfigManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self, config_yaml_path: Optional[Path] = None) -> Settings:
        """Load YAML, merge with env, build and validate Settings."""
        yaml_path = config_yaml_path or _CONFIG_YAML_PATH
        self._yaml_data = self._load_yaml(yaml_path)

        # Merge yaml → overrides → pass as init overrides
        merged = {**self._yaml_data, **self._overrides}
        self._settings = Settings(overrides=merged)
        self._settings.validate()
        self._initialized_at = datetime.now(UTC)
        return self._settings

    def get(self) -> Settings:
        """Return the current Settings instance, initializing lazily if needed."""
        if self._settings is None:
            self.initialize()
        return self._settings  # type: ignore[return-value]

    def set_override(self, key: str, value: Any) -> None:
        """Apply a runtime override and rebuild Settings immediately."""
        self._overrides[key] = value
        if self._settings is not None:
            merged = {**self._yaml_data, **self._overrides}
            self._settings = Settings(overrides=merged)

    def clear_override(self, key: str) -> None:
        """Remove a runtime override."""
        self._overrides.pop(key, None)
        if self._settings is not None:
            merged = {**self._yaml_data, **self._overrides}
            self._settings = Settings(overrides=merged)

    def reload(self, config_yaml_path: Optional[Path] = None) -> Settings:
        """Hot-reload configuration from disk without restarting."""
        self._settings = None
        return self.initialize(config_yaml_path)

    def export_snapshot(self) -> Dict[str, Any]:
        """Export current full settings as a serializable dict (masks secrets)."""
        if self._settings is None:
            self.initialize()
        snap = self._settings.to_dict()  # type: ignore[union-attr]
        # Mask sensitive fields
        for field in ("secret_key", "llm_api_key"):
            if field in snap and snap[field]:
                snap[field] = "***"
        snap["_snapshot_at"] = datetime.now(UTC).isoformat()
        snap["_initialized_at"] = self._initialized_at.isoformat() if self._initialized_at else None
        return snap

    # ─── Private helpers ───────────────────────────────────────────────

    @staticmethod
    def _load_yaml(path: Path) -> Dict[str, Any]:
        if not _YAML_AVAILABLE or not path.exists():
            return {}
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            return {k.upper(): v for k, v in data.items()}  # normalize keys
        except Exception:
            return {}


# ── Module-level singleton ─────────────────────────────────────────────────────
_config_manager = ConfigManager()
