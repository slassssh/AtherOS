"""
AtherOS v1.0.0-rc1 — Backup Manager

Provides atomic backup and restore for all AtherOS persistent state:
  - SQLite database (.db → .db.gz compressed copy)
  - Memory snapshot (memory.json)
  - Knowledge Graph export (context_graph.json via ContextManager)
  - Configuration files (atheros_config.json, config.yaml)
  - Plugin manifests directory
  - Settings snapshot
"""
from __future__ import annotations

import gzip
import json
import shutil
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.app.backup.types import BackupManifest
from backend.app.utils.logger import logger


class BackupManager:
    """
    Manages versioned backups and full restore capability for AtherOS.

    Each backup is stored in:
      <backup_dir>/<label>_<timestamp>_<id>/
    with a manifest.json describing the archive contents.
    """

    def __init__(
        self,
        backup_dir: Optional[Path] = None,
        context_manager: Any = None,
        memory_manager: Any = None,
    ) -> None:
        self._backup_root = backup_dir or Path("backups")
        self._backup_root.mkdir(parents=True, exist_ok=True)
        self._context_manager = context_manager
        self._memory_manager = memory_manager

    def backup(self, label: str = "manual") -> BackupManifest:
        """
        Create a versioned backup archive. Returns the BackupManifest.
        """
        ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        manifest = BackupManifest(label=label)
        target_dir = self._backup_root / f"{label}_{ts}_{manifest.backup_id}"
        target_dir.mkdir(parents=True, exist_ok=True)
        manifest.backup_dir = str(target_dir)

        files: List[str] = []
        total_bytes = 0

        # 1. SQLite database
        for db_name in ("atheros.db",):
            db_path = Path(db_name)
            if db_path.exists():
                dest = target_dir / f"{db_name}.gz"
                self._compress_file(db_path, dest)
                files.append(dest.name)
                total_bytes += dest.stat().st_size

        # 2. Memory snapshot
        for mem_file in ("memory.json", "memory_backup.json"):
            mem_path = Path(mem_file)
            if mem_path.exists():
                dest = target_dir / mem_file
                shutil.copy2(mem_path, dest)
                files.append(dest.name)
                total_bytes += dest.stat().st_size

        # 3. Knowledge Graph export
        graph_export = self._export_knowledge_graph()
        if graph_export:
            graph_path = target_dir / "context_graph.json"
            graph_path.write_text(json.dumps(graph_export, indent=2, default=str), encoding="utf-8")
            files.append("context_graph.json")
            total_bytes += graph_path.stat().st_size

        # 4. Configuration files
        for cfg_name in ("atheros_config.json", "config.yaml"):
            cfg_path = Path(cfg_name)
            if cfg_path.exists():
                dest = target_dir / cfg_name
                shutil.copy2(cfg_path, dest)
                files.append(cfg_name)
                total_bytes += dest.stat().st_size

        # 5. Plugin manifests directory
        plugin_dir = Path("plugins")
        if plugin_dir.exists() and plugin_dir.is_dir():
            dest_plugins = target_dir / "plugins"
            shutil.copytree(plugin_dir, dest_plugins, dirs_exist_ok=True)
            files.append("plugins/")
            total_bytes += sum(f.stat().st_size for f in dest_plugins.rglob("*") if f.is_file())

        # 6. Settings snapshot
        settings_snap = self._export_settings()
        settings_path = target_dir / "settings_snapshot.json"
        settings_path.write_text(json.dumps(settings_snap, indent=2, default=str), encoding="utf-8")
        files.append("settings_snapshot.json")
        total_bytes += settings_path.stat().st_size

        # 7. Write manifest
        manifest.files = files
        manifest.size_bytes = total_bytes
        manifest.metadata = {
            "label": label,
            "backup_dir": str(target_dir),
            "file_count": len(files),
        }
        manifest_path = target_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest.to_dict(), indent=2), encoding="utf-8")

        logger.info(
            f"Backup '{label}' created: {target_dir} ({len(files)} files, {total_bytes:,} bytes)"
        )
        return manifest

    def restore(self, backup_dir: Path) -> bool:
        """
        Restore AtherOS from a backup directory.
        Returns True on success, False on failure.
        """
        if not backup_dir.exists():
            logger.error(f"Restore failed: backup directory not found: {backup_dir}")
            return False

        manifest_path = backup_dir / "manifest.json"
        if not manifest_path.exists():
            logger.error(f"Restore failed: manifest.json not found in {backup_dir}")
            return False

        try:
            manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            logger.info(f"Restoring backup '{manifest_data.get('label', '?')}' from {backup_dir}")

            # Restore database
            for gz_name in backup_dir.glob("*.db.gz"):
                original = gz_name.stem  # removes .gz
                self._decompress_file(gz_name, Path(original))
                logger.info(f"  Restored database: {original}")

            # Restore memory files
            for mem_name in ("memory.json", "memory_backup.json"):
                src = backup_dir / mem_name
                if src.exists():
                    shutil.copy2(src, Path(mem_name))
                    logger.info(f"  Restored: {mem_name}")

            # Restore config files
            for cfg_name in ("atheros_config.json", "config.yaml"):
                src = backup_dir / cfg_name
                if src.exists():
                    shutil.copy2(src, Path(cfg_name))
                    logger.info(f"  Restored: {cfg_name}")

            # Restore plugins
            src_plugins = backup_dir / "plugins"
            if src_plugins.exists():
                shutil.copytree(src_plugins, Path("plugins"), dirs_exist_ok=True)
                logger.info("  Restored: plugins/")

            logger.info(f"Restore complete from '{backup_dir}'")
            return True

        except Exception as exc:
            logger.exception(f"Restore failed: {exc}")
            return False

    def list_backups(self) -> List[BackupManifest]:
        """List all available backups with their manifests."""
        manifests: List[BackupManifest] = []
        for manifest_path in sorted(self._backup_root.rglob("manifest.json"), reverse=True):
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                m = BackupManifest(
                    backup_id=data.get("backup_id", "?"),
                    label=data.get("label", "?"),
                    atheros_version=data.get("atheros_version", "?"),
                    backup_dir=data.get("backup_dir", str(manifest_path.parent)),
                    files=data.get("files", []),
                    size_bytes=data.get("size_bytes", 0),
                    metadata=data.get("metadata", {}),
                )
                manifests.append(m)
            except Exception:
                continue
        return manifests

    def delete_backup(self, backup_id: str) -> bool:
        """Delete a backup by its ID. Returns True if deleted."""
        for manifest_path in self._backup_root.rglob("manifest.json"):
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                if data.get("backup_id") == backup_id:
                    shutil.rmtree(manifest_path.parent)
                    logger.info(f"Deleted backup {backup_id}: {manifest_path.parent}")
                    return True
            except Exception:
                continue
        return False

    # ─── Private helpers ───────────────────────────────────────────────

    @staticmethod
    def _compress_file(src: Path, dest: Path) -> None:
        with src.open("rb") as f_in, gzip.open(dest, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    @staticmethod
    def _decompress_file(src: Path, dest: Path) -> None:
        with gzip.open(src, "rb") as f_in, dest.open("wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    def _export_knowledge_graph(self) -> Dict[str, Any]:
        if self._context_manager is None:
            return {}
        try:
            graph = self._context_manager._graph
            nodes = {nid: n.to_dict() for nid, n in graph._nodes.items()}
            edges = [e.to_dict() for e in graph._edges]
            return {"nodes": nodes, "edges": edges}
        except Exception:
            return {}

    def _export_settings(self) -> Dict[str, Any]:
        try:
            from backend.app.config.config_manager import _config_manager
            return _config_manager.export_snapshot()
        except Exception:
            return {}
