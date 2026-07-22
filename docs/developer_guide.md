# AtherOS v1.0.0-rc1 — Developer Guide

## Development Setup

```bash
git clone https://github.com/slassssh/AtherOS
cd AtherOS
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
pip install ruff black mypy bandit pytest-cov
cp .env.example .env
```

---

## Running Tests

```bash
# Full stage regression (90 tests)
python -m pytest backend/tests/test_stage2_pipeline.py \
    backend/tests/test_stage3_api.py \
    backend/tests/test_stage4_llm.py \
    backend/tests/test_stage5_security.py \
    backend/tests/test_stage6_database.py \
    backend/tests/test_stage7_memory.py \
    backend/tests/test_stage8_graph.py \
    backend/tests/test_stage9_agents.py \
    backend/tests/test_stage10_event_bus.py \
    backend/tests/test_stage11_plugins.py \
    backend/tests/test_stage12_desktop.py \
    backend/tests/test_stage13_model_orchestrator.py \
    backend/tests/test_stage14_cluster.py \
    backend/tests/test_stage15_rc1.py \
    -v

# With coverage
python -m pytest backend/tests/test_stage15_rc1.py \
    --cov=backend/app --cov-report=html:coverage_report -v
```

---

## Code Quality Gates

```bash
# Lint
ruff check backend/

# Format check
black --check backend/

# Auto-format
black backend/

# Type check
mypy backend/ --ignore-missing-imports

# Security scan
bandit -r backend/ -ll --exclude backend/tests/

# Dependency audit
pip-audit -r requirements.txt
```

---

## Benchmark Suite

```bash
python -m backend.benchmarks
# → Outputs benchmark_report.json and benchmark_report.md
```

---

## Project Structure

```
AtherOS/
├── backend/
│   ├── app/
│   │   ├── agents/          # Multi-Agent Runtime (Stage 9)
│   │   ├── api/             # FastAPI Service Layer (Stage 3)
│   │   ├── backup/          # Backup & Restore (Stage 15)
│   │   ├── cluster/         # Distributed Runtime (Stage 14)
│   │   ├── config/          # Configuration System (Stage 15)
│   │   ├── context/         # Knowledge Graph (Stage 8)
│   │   ├── core/            # Engine, Journal, Session, StateMachine
│   │   ├── database/        # SQLAlchemy Persistence (Stage 6)
│   │   ├── events/          # Event Bus (Stage 10)
│   │   ├── health/          # Health Diagnostics (Stage 15)
│   │   ├── llm/             # LLM + Model Orchestrator (Stage 4, 13)
│   │   ├── memory/          # 7-Layer Memory (Stage 7)
│   │   ├── planner/         # Goal Planner (Stage 2)
│   │   ├── plugins/         # Plugin SDK (Stage 11)
│   │   ├── registry/        # Capability Registry (Stage 10)
│   │   ├── tools/           # Sandboxed Tools (Stage 5)
│   │   └── utils/           # Logger, Exceptions, CrashReporter
│   ├── benchmarks/          # Benchmark Suite (Stage 15)
│   └── tests/               # Test Suite (all stages)
├── desktop/                 # PyQt6 Desktop (Stage 12)
├── docs/                    # Documentation
├── scripts/                 # Build scripts
├── .github/workflows/       # CI/CD Pipelines
├── Dockerfile               # Production Docker image
├── docker-compose.yml       # Docker Compose
├── pyproject.toml           # Project + tool configs
└── VERSION                  # 1.0.0-rc1
```

---

## Architecture Principles

1. **Engine communicates ONLY via public interfaces** — never direct module imports across subsystem boundaries
2. **Memory access ONLY through MemoryManager** — no direct memory storage access
3. **Tools ONLY through ToolExecutor** — never instantiated directly
4. **Events ONLY through EventBus** — no polling between modules
5. **Agents NEVER communicate directly** — all messages through AgentManager

---

## Adding a New Subsystem

1. Create `backend/app/<subsystem>/` with `manager.py`, `types.py`, `__init__.py`
2. Register in `Engine.__init__()` as an injected dependency
3. Register in `Engine._register_subsystem_capabilities()`
4. Wire into `HealthManager.full_report()`
5. Add tests to `backend/tests/test_stage<N>_<name>.py`
