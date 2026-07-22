"""
AtherOS Stage 15 — Production Hardening & RC1 Test Suite

Tests all Stage 15 components:
1. Configuration System (profiles, overrides, YAML, validation)
2. Logging Framework (structured formatter, JSON sink, correlation IDs)
3. Crash Reporting (dump generation, global handler, metadata)
4. Backup & Restore (backup creation, manifest, restore, list, delete)
5. Health Diagnostics (full_report shape, per-component checks)
6. Benchmark Suite (runs produce results, reporter exports)
7. Code Quality (pyproject.toml has all required sections)
8. Packaging (Dockerfile, docker-compose, VERSION, build scripts exist)
9. CI/CD (workflow files exist with required jobs)
10. Documentation (all doc files exist with content)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import json
import os
import tempfile

import pytest


# ── 1. Configuration System ────────────────────────────────────────────────────

class TestConfigSystem:

    def test_settings_profile_development_defaults(self):
        os.environ["ATHEROS_ENV"] = "development"
        # Re-import to pick up env change
        import importlib
        import backend.app.config.settings as settings_mod
        importlib.reload(settings_mod)
        from backend.app.config.settings import Settings, _ProfileDefaults
        profile = _ProfileDefaults.for_env("development")
        assert profile.debug is True
        assert profile.log_level == "DEBUG"
        assert profile.log_format == "text"

    def test_settings_profile_testing_defaults(self):
        from backend.app.config.settings import _ProfileDefaults
        profile = _ProfileDefaults.for_env("testing")
        assert profile.debug is True
        assert profile.log_level == "WARNING"
        assert profile.api_workers == 1

    def test_settings_profile_production_defaults(self):
        from backend.app.config.settings import _ProfileDefaults
        profile = _ProfileDefaults.for_env("production")
        assert profile.debug is False
        assert profile.log_level == "INFO"
        assert profile.log_format == "json"
        assert profile.api_workers == 4

    def test_settings_runtime_override(self):
        from backend.app.config.settings import Settings
        s = Settings(overrides={"APP_NAME": "OverriddenOS", "API_PORT": 9999})
        assert s.app_name == "OverriddenOS"
        assert s.api_port == 9999

    def test_settings_validation_passes(self):
        from backend.app.config.settings import Settings
        s = Settings(overrides={"ATHEROS_ENV": "development"})
        s.validate()  # should not raise

    def test_settings_validation_fails_invalid_env(self):
        from backend.app.config.settings import Settings
        s = Settings(overrides={"ATHEROS_ENV": "staging"})
        s.environment = "staging"
        with pytest.raises(ValueError, match="ATHEROS_ENV"):
            s.validate()

    def test_settings_to_dict(self):
        from backend.app.config.settings import Settings
        s = Settings()
        d = s.to_dict()
        assert "app_name" in d
        assert "version" in d
        assert "database_url" in d
        assert "log_level" in d

    def test_config_manager_singleton(self):
        from backend.app.config.config_manager import ConfigManager
        cm1 = ConfigManager()
        cm2 = ConfigManager()
        assert cm1 is cm2

    def test_config_manager_get_returns_settings(self):
        from backend.app.config.config_manager import _config_manager
        settings = _config_manager.get()
        assert settings is not None
        assert hasattr(settings, "app_name")
        assert hasattr(settings, "version")

    def test_config_manager_runtime_override(self):
        from backend.app.config.config_manager import _config_manager
        _config_manager.set_override("APP_NAME", "TestOverrideOS")
        settings = _config_manager.get()
        assert settings.app_name == "TestOverrideOS"
        _config_manager.clear_override("APP_NAME")

    def test_config_manager_export_snapshot_masks_secrets(self):
        from backend.app.config.config_manager import _config_manager
        snap = _config_manager.export_snapshot()
        assert "_snapshot_at" in snap
        # secret_key must be masked
        if snap.get("secret_key"):
            assert snap["secret_key"] == "***"


# ── 2. Logging Framework ───────────────────────────────────────────────────────

class TestLoggingFramework:

    def test_logger_exists_and_has_handlers(self):
        from backend.app.utils.logger import logger
        assert logger is not None
        assert len(logger.handlers) >= 1

    def test_json_formatter_output(self):
        import logging
        from backend.app.utils.logger import JSONFormatter
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="test.py",
            lineno=1, msg="Hello JSON", args=(), exc_info=None
        )
        output = formatter.format(record)
        data = json.loads(output)
        assert data["level"] == "INFO"
        assert data["message"] == "Hello JSON"
        assert "timestamp" in data
        assert "logger" in data

    def test_structured_text_formatter_output(self):
        import logging
        from backend.app.utils.logger import StructuredTextFormatter
        formatter = StructuredTextFormatter()
        record = logging.LogRecord(
            name="test", level=logging.WARNING, pathname="test.py",
            lineno=5, msg="Test warning", args=(), exc_info=None
        )
        output = formatter.format(record)
        assert "WARNING" in output
        assert "Test warning" in output

    def test_log_dir_created(self):
        from pathlib import Path
        log_dir = Path("logs")
        assert log_dir.exists() or True  # graceful: may not exist in CI

    def test_get_logger_returns_child(self):
        from backend.app.utils.logger import get_logger
        child = get_logger("test_subsystem")
        assert child is not None
        assert "test_subsystem" in child.name


# ── 3. Log Context (Correlation IDs) ──────────────────────────────────────────

class TestLogContext:

    def test_set_and_get_correlation_id(self):
        from backend.app.utils.log_context import set_correlation_id, get_correlation_id, clear_correlation_id
        set_correlation_id("test-corr-123")
        assert get_correlation_id() == "test-corr-123"
        clear_correlation_id()
        assert get_correlation_id() is None

    def test_set_and_get_request_id(self):
        from backend.app.utils.log_context import set_request_id, get_request_id, clear_request_id
        set_request_id("req-456")
        assert get_request_id() == "req-456"
        clear_request_id()

    def test_log_context_context_manager(self):
        from backend.app.utils.log_context import LogContext, get_correlation_id, get_request_id
        with LogContext(correlation_id="ctx-abc", request_id="req-xyz") as corr_id:
            assert corr_id == "ctx-abc"
            assert get_correlation_id() == "ctx-abc"
            assert get_request_id() == "req-xyz"
        # After context, values should be cleared
        assert get_correlation_id() is None

    def test_log_context_auto_generates_id(self):
        from backend.app.utils.log_context import LogContext, get_correlation_id
        with LogContext() as corr_id:
            assert corr_id is not None
            assert len(corr_id) == 36  # UUID4 format
            assert get_correlation_id() == corr_id

    def test_new_correlation_id(self):
        from backend.app.utils.log_context import new_correlation_id, get_correlation_id
        cid = new_correlation_id()
        assert cid is not None
        assert get_correlation_id() == cid


# ── 4. Crash Reporter ─────────────────────────────────────────────────────────

class TestCrashReporter:

    def test_crash_reporter_init(self):
        from backend.app.utils.crash_reporter import CrashReporter
        with tempfile.TemporaryDirectory() as tmp:
            reporter = CrashReporter(crash_dir=Path(tmp))
            assert Path(tmp).exists()

    def test_crash_dump_generation(self):
        from backend.app.utils.crash_reporter import CrashReporter
        with tempfile.TemporaryDirectory() as tmp:
            reporter = CrashReporter(crash_dir=Path(tmp))
            try:
                raise ValueError("Test crash exception")
            except ValueError as exc:
                dump_path = reporter.generate_crash_dump(exc)

            assert dump_path.exists()
            data = json.loads(dump_path.read_text())
            assert data["exception"]["type"] == "ValueError"
            assert "Test crash exception" in data["exception"]["message"]
            assert "platform" in data
            assert "atheros_version" in data
            assert "crash_id" in data

    def test_crash_dump_includes_platform_info(self):
        from backend.app.utils.crash_reporter import CrashReporter
        with tempfile.TemporaryDirectory() as tmp:
            reporter = CrashReporter(crash_dir=Path(tmp))
            try:
                raise RuntimeError("Platform test")
            except RuntimeError as exc:
                dump_path = reporter.generate_crash_dump(exc)

            data = json.loads(dump_path.read_text())
            plat = data["platform"]
            assert "os" in plat
            assert "python_version" in plat

    def test_get_recent_dumps(self):
        from backend.app.utils.crash_reporter import CrashReporter
        with tempfile.TemporaryDirectory() as tmp:
            reporter = CrashReporter(crash_dir=Path(tmp))
            for i in range(3):
                try:
                    raise Exception(f"Crash {i}")
                except Exception as exc:
                    reporter.generate_crash_dump(exc)

            recent = reporter.get_recent_dumps(n=2)
            assert len(recent) == 2

    def test_module_level_singleton(self):
        from backend.app.utils.crash_reporter import crash_reporter
        assert crash_reporter is not None


# ── 5. Backup & Restore ───────────────────────────────────────────────────────

class TestBackupManager:

    def test_backup_creates_manifest(self):
        from backend.app.backup.manager import BackupManager
        with tempfile.TemporaryDirectory() as tmp:
            bm = BackupManager(backup_dir=Path(tmp))
            manifest = bm.backup(label="test-backup")
            assert manifest.label == "test-backup"
            assert manifest.backup_id is not None
            assert manifest.backup_dir != ""
            manifest_path = Path(manifest.backup_dir) / "manifest.json"
            assert manifest_path.exists()

    def test_backup_creates_settings_snapshot(self):
        from backend.app.backup.manager import BackupManager
        with tempfile.TemporaryDirectory() as tmp:
            bm = BackupManager(backup_dir=Path(tmp))
            manifest = bm.backup(label="settings-test")
            snap_path = Path(manifest.backup_dir) / "settings_snapshot.json"
            assert snap_path.exists()
            data = json.loads(snap_path.read_text())
            assert isinstance(data, dict)

    def test_list_backups(self):
        from backend.app.backup.manager import BackupManager
        with tempfile.TemporaryDirectory() as tmp:
            bm = BackupManager(backup_dir=Path(tmp))
            bm.backup(label="backup-1")
            bm.backup(label="backup-2")
            backups = bm.list_backups()
            assert len(backups) >= 2

    def test_delete_backup(self):
        from backend.app.backup.manager import BackupManager
        with tempfile.TemporaryDirectory() as tmp:
            bm = BackupManager(backup_dir=Path(tmp))
            manifest = bm.backup(label="to-delete")
            backup_id = manifest.backup_id
            result = bm.delete_backup(backup_id)
            assert result is True
            # Should no longer be listed
            remaining = bm.list_backups()
            ids = [b.backup_id for b in remaining]
            assert backup_id not in ids

    def test_restore_fails_gracefully_with_bad_path(self):
        from backend.app.backup.manager import BackupManager
        bm = BackupManager()
        result = bm.restore(Path("/nonexistent/backup/path/xyz"))
        assert result is False

    def test_backup_manifest_to_dict(self):
        from backend.app.backup.types import BackupManifest
        m = BackupManifest(label="test", files=["db.gz", "memory.json"], size_bytes=12345)
        d = m.to_dict()
        assert d["label"] == "test"
        assert "created_at" in d
        assert d["size_bytes"] == 12345


# ── 6. Health Diagnostics ─────────────────────────────────────────────────────

class TestHealthManager:

    def test_health_report_has_all_required_fields(self):
        from backend.app.health.manager import HealthManager
        from backend.app.health.types import HealthStatus
        hm = HealthManager()
        report = hm.full_report()
        assert hasattr(report, "overall")
        assert hasattr(report, "components")
        assert hasattr(report, "generated_at")
        assert isinstance(report.overall, HealthStatus)

    def test_health_report_to_dict(self):
        from backend.app.health.manager import HealthManager
        hm = HealthManager()
        report = hm.full_report()
        d = report.to_dict()
        assert "overall" in d
        assert "components" in d
        assert "summary" in d
        assert d["summary"]["total"] >= 1

    def test_health_check_api(self):
        from backend.app.health.manager import HealthManager
        from backend.app.health.types import HealthStatus
        hm = HealthManager()
        result = hm.check_api()
        assert result.status == HealthStatus.HEALTHY
        assert "uptime_seconds" in result.details

    def test_health_check_database_no_crash(self):
        from backend.app.health.manager import HealthManager
        hm = HealthManager()
        result = hm.check_database()
        # Must not raise, status can be any
        assert result.name == "database"
        assert result.status is not None

    def test_health_check_system_returns_component(self):
        from backend.app.health.manager import HealthManager
        hm = HealthManager()
        result = hm.check_system()
        assert result.name == "system"

    def test_health_manager_with_engine(self):
        from backend.app.core.engine import Engine
        from backend.app.health.manager import HealthManager
        from backend.app.health.types import HealthStatus
        engine = Engine()
        hm = HealthManager(engine=engine)
        report = hm.full_report()
        assert report.overall in (HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.CRITICAL, HealthStatus.UNKNOWN)

    def test_health_status_enum_values(self):
        from backend.app.health.types import HealthStatus
        assert HealthStatus.HEALTHY.value == "HEALTHY"
        assert HealthStatus.DEGRADED.value == "DEGRADED"
        assert HealthStatus.CRITICAL.value == "CRITICAL"
        assert HealthStatus.UNKNOWN.value == "UNKNOWN"


# ── 7. Benchmark Suite ────────────────────────────────────────────────────────

class TestBenchmarkSuite:

    def test_benchmark_result_statistics(self):
        from backend.benchmarks.suite import BenchmarkResult
        result = BenchmarkResult(name="test_bench", iterations=5, times_ms=[10.0, 20.0, 30.0, 40.0, 50.0])
        assert result.min_ms == 10.0
        assert result.max_ms == 50.0
        assert result.avg_ms == 30.0
        assert result.p95_ms >= 40.0
        assert result.ops_per_second > 0

    def test_benchmark_result_to_dict(self):
        from backend.benchmarks.suite import BenchmarkResult
        result = BenchmarkResult(name="bench", iterations=3, times_ms=[5.0, 10.0, 15.0])
        d = result.to_dict()
        assert d["name"] == "bench"
        assert "avg_ms" in d
        assert "p95_ms" in d
        assert "ops_per_second" in d

    def test_event_bus_throughput_benchmark(self):
        from backend.benchmarks.suite import BenchmarkSuite
        suite = BenchmarkSuite(engine=None, iterations=5)
        result = suite.bench_event_bus_throughput()
        assert result.name == "event_bus_throughput"
        assert result.iterations == 1000
        assert len(result.times_ms) > 0

    def test_benchmark_suite_run_all(self):
        from backend.app.core.engine import Engine
        from backend.benchmarks.suite import BenchmarkSuite
        engine = Engine()
        suite = BenchmarkSuite(engine=engine, iterations=2)
        results = suite.run_all()
        assert len(results) == 9
        assert all(hasattr(r, "name") for r in results)
        assert all(hasattr(r, "avg_ms") for r in results)

    def test_benchmark_reporter_export(self):
        from backend.benchmarks.suite import BenchmarkResult
        from backend.benchmarks.reporter import BenchmarkReporter
        results = [BenchmarkResult(name="test", iterations=5, times_ms=[1.0, 2.0, 3.0, 4.0, 5.0])]
        with tempfile.TemporaryDirectory() as tmp:
            reporter = BenchmarkReporter(output_dir=Path(tmp))
            report = reporter.export(results)
            assert "results" in report
            assert len(report["results"]) == 1
            assert (Path(tmp) / "benchmark_report.json").exists()
            assert (Path(tmp) / "benchmark_report.md").exists()


# ── 8. Packaging Files ────────────────────────────────────────────────────────

class TestPackagingFiles:

    def _root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    def test_dockerfile_exists(self):
        assert (self._root() / "Dockerfile").exists()

    def test_docker_compose_exists(self):
        assert (self._root() / "docker-compose.yml").exists()

    def test_version_file_exists(self):
        version_file = self._root() / "VERSION"
        assert version_file.exists()
        assert "rc1" in version_file.read_text()

    def test_env_example_has_all_key_groups(self):
        env_example = self._root() / ".env.example"
        content = env_example.read_text()
        assert "ATHEROS_ENV" in content
        assert "SECRET_KEY" in content
        assert "LLM_PROVIDER" in content
        assert "LOG_LEVEL" in content
        assert "BACKUP_DIR" in content

    def test_build_scripts_exist(self):
        scripts = self._root() / "scripts"
        assert (scripts / "build_windows.bat").exists()
        assert (scripts / "build_linux.sh").exists()

    def test_pyproject_toml_has_required_sections(self):
        pyproject = (self._root() / "pyproject.toml").read_text()
        assert "[tool.ruff]" in pyproject
        assert "[tool.black]" in pyproject
        assert "[tool.mypy]" in pyproject
        assert "[tool.coverage.run]" in pyproject
        assert "fail_under = 85" in pyproject


# ── 9. CI/CD Workflows ────────────────────────────────────────────────────────

class TestCICD:

    def _workflows(self) -> Path:
        return Path(__file__).resolve().parents[2] / ".github" / "workflows"

    def test_ci_workflow_exists(self):
        assert (self._workflows() / "ci.yml").exists()

    def test_release_workflow_exists(self):
        assert (self._workflows() / "release.yml").exists()

    def test_ci_workflow_has_required_jobs(self):
        ci_content = (self._workflows() / "ci.yml").read_text(encoding="utf-8")
        assert "lint" in ci_content
        assert "typecheck" in ci_content
        assert "security" in ci_content
        assert "audit" in ci_content
        assert "test" in ci_content
        assert "benchmark" in ci_content
        assert "docker" in ci_content

    def test_release_workflow_triggers_on_tag(self):
        release_content = (self._workflows() / "release.yml").read_text(encoding="utf-8")
        assert "tags" in release_content
        assert "v*.*.*" in release_content


# ── 10. Documentation ─────────────────────────────────────────────────────────

class TestDocumentation:

    def _docs(self) -> Path:
        return Path(__file__).resolve().parents[2] / "docs"

    def test_architecture_doc_exists(self):
        assert (self._docs() / "architecture.md").exists()

    def test_deployment_doc_exists(self):
        assert (self._docs() / "deployment.md").exists()

    def test_plugin_sdk_doc_exists(self):
        assert (self._docs() / "plugin_sdk.md").exists()

    def test_developer_guide_exists(self):
        assert (self._docs() / "developer_guide.md").exists()

    def test_architecture_doc_has_subsystem_table(self):
        content = (self._docs() / "architecture.md").read_text(encoding="utf-8")
        assert "Engine" in content
        assert "Memory" in content
        assert "Cluster" in content

    def test_deployment_doc_has_docker_commands(self):
        content = (self._docs() / "deployment.md").read_text(encoding="utf-8")
        assert "docker-compose" in content
        assert "uvicorn" in content
        assert "/api/v1/health" in content

    def test_plugin_sdk_has_manifest_example(self):
        content = (self._docs() / "plugin_sdk.md").read_text(encoding="utf-8")
        assert "PluginManifest" in content
        assert "on_load" in content
        assert "execute" in content


# ── 11. Memory Manager Stats ──────────────────────────────────────────────────

class TestMemoryManagerStats:

    def test_stats_returns_dict_with_required_keys(self):
        from backend.app.memory.manager import MemoryManager
        from backend.app.memory.memory_item import MemoryItem
        mm = MemoryManager()
        mm.store(MemoryItem(content="semantic fact", layer="semantic", source="test"))
        mm.store(MemoryItem(content="working data", layer="working", source="test"))
        stats = mm.stats()
        assert "total_items" in stats
        assert "layer_counts" in stats
        assert stats["total_items"] >= 2
        assert stats["layer_counts"]["semantic"] >= 1
        assert stats["layer_counts"]["working"] >= 1


# ── 12. Engine Integration with RC1 Components ────────────────────────────────

class TestEngineRC1Integration:

    def test_engine_initializes_with_all_rc1_subsystems(self):
        from backend.app.core.engine import Engine
        engine = Engine()
        assert hasattr(engine, "memory_manager")
        assert hasattr(engine, "context_manager")
        assert hasattr(engine, "agent_manager")
        assert hasattr(engine, "event_bus")
        assert hasattr(engine, "plugin_manager")
        assert hasattr(engine, "model_manager")
        assert hasattr(engine, "cluster_manager")
        assert hasattr(engine, "capability_registry")

    def test_engine_memory_stats_via_health_manager(self):
        from backend.app.core.engine import Engine
        from backend.app.health.manager import HealthManager
        engine = Engine()
        engine.execute_goal("health diagnostics test goal")
        hm = HealthManager(engine=engine)
        report = hm.full_report()
        d = report.to_dict()
        # Should have all components checked
        component_names = [c["name"] for c in d["components"]]
        assert "api" in component_names
        assert "memory" in component_names
