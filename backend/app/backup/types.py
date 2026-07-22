"""AtherOS Backup — Type definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4


@dataclass
class BackupManifest:
    """Describes a single AtherOS backup archive."""

    backup_id: str = field(default_factory=lambda: str(uuid4())[:8])
    label: str = "backup"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    atheros_version: str = "1.0.0-rc1"
    backup_dir: str = ""
    files: List[str] = field(default_factory=list)
    size_bytes: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "backup_id": self.backup_id,
            "label": self.label,
            "created_at": self.created_at.isoformat(),
            "atheros_version": self.atheros_version,
            "backup_dir": self.backup_dir,
            "files": self.files,
            "size_bytes": self.size_bytes,
            "metadata": self.metadata,
        }
