# AtherOS v1.0.0-rc1 — Architecture Guide

## Overview

AtherOS is a **production AI Operating System** built on Python 3.13, designed for autonomous goal execution via a hierarchical multi-agent runtime. It provides a unified platform for orchestrating AI providers, tools, memory, planning, and distributed execution.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AtherOS v1.0.0-rc1                                 │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      Desktop GUI (PyQt6)                             │  │
│  │  MainWindow · Console · Agent Dashboard · Memory Explorer            │  │
│  │  Knowledge Graph Viewer · Event Timeline · Plugin Manager            │  │
│  └────────────────────────┬─────────────────────────────────────────────┘  │
│                           │ HTTP REST + WebSocket                           │
│  ┌────────────────────────▼─────────────────────────────────────────────┐  │
│  │                FastAPI Service Layer (port 8000)                      │  │
│  │  /health · /health/detailed · /goals/execute · /sessions             │  │
│  │  /memory · /backups · /capabilities · /events/history · /ws          │  │
│  └────────────────────────┬─────────────────────────────────────────────┘  │
│                           │                                                 │
│  ┌────────────────────────▼─────────────────────────────────────────────┐  │
│  │                      Engine Core                                      │  │
│  │   StateMachine · Journal · Session · ToolExecutor · Planner           │  │
│  └───┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────┘  │
│      │      │      │      │      │      │      │      │      │             │
│   Mem    Graph  Agents EventBus Plugins Models Cluster Health  Config      │
│  Mgr    Mgr    Mgr    (S10)   (S11)   (S13)  (S14)  (S15)   (S15)         │
│  (S7)   (S8)   (S9)                                                        │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │               SQLAlchemy SQLite Persistence Layer                    │  │
│  │   Sessions · JournalEvents · MemoryItems · Plans · Tasks             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Subsystems

| Subsystem | Module | Stage | Description |
|-----------|--------|-------|-------------|
| Engine | `backend/app/core/engine.py` | 2 | Central orchestrator, coordinates all subsystems |
| Planner | `backend/app/planner/` | 2 | Goal decomposition into Task DAGs |
| Tool Executor | `backend/app/core/tool_executor.py` | 2 | Sandboxed tool invocation gateway |
| FastAPI API | `backend/app/api/` | 3 | REST + WebSocket service layer |
| LLM Layer | `backend/app/llm/` | 4 | Multi-provider LLM abstraction |
| Security | `backend/app/tools/` | 5 | Hardened tool sandbox + permissions |
| Database | `backend/app/database/` | 6 | SQLAlchemy SQLite persistence |
| Memory | `backend/app/memory/` | 7 | 7-layer hierarchical memory system |
| Context Graph | `backend/app/context/` | 8 | Native knowledge graph with BFS/DFS |
| Agent Runtime | `backend/app/agents/` | 9 | 8 autonomous specialist agents |
| Event Bus | `backend/app/events/` | 10 | Pub/sub nervous system |
| Plugin SDK | `backend/app/plugins/` | 11 | Lifecycle-managed plugin framework |
| Desktop | `desktop/` | 12 | PyQt6 AI Operating Environment |
| Model Orchestrator | `backend/app/llm/orchestrator.py` | 13 | AI routing, fallback, telemetry |
| Cluster | `backend/app/cluster/` | 14 | Distributed runtime + leader election |
| Config Manager | `backend/app/config/` | 15 | 4-layer config resolution |
| Health Manager | `backend/app/health/` | 15 | Unified diagnostics |
| Backup Manager | `backend/app/backup/` | 15 | Atomic backup + restore |
| Crash Reporter | `backend/app/utils/crash_reporter.py` | 15 | Global exception capture |
| Benchmark Suite | `backend/benchmarks/` | 15 | Latency + throughput profiling |

---

## Memory Architecture (7 Layers)

```
Session Memory    ← current conversation context
Working Memory    ← current execution state
Project Memory    ← project-scoped facts
Long-Term Memory  ← persistent user knowledge
Episodic Memory   ← past execution records
Semantic Memory   ← facts and concepts
Tool Memory       ← tool output cache
```

---

## Event Flow

```
User Goal
  → Engine.execute_goal()
  → EventBus.publish(GOAL_CREATED)
  → Planner.create_plan()
  → EventBus.publish(TASK_CREATED × N)
  → ToolExecutor.execute()
  → MemoryManager.store()
  → ContextManager.update_node()
  → EventBus.publish(TASK_COMPLETED)
  → EventBus.publish(GOAL_COMPLETED)
  → WebSocket broadcast to desktop/clients
```

---

## Security Model

- **FileTool**: Workspace sandbox root enforcement, path traversal prevention
- **TerminalTool**: Allowlist-only executables, no shell=True, timeout enforcement
- **PythonTool**: Isolated subprocess execution, restricted builtins
- **API**: Request ID correlation, structured error responses, CORS middleware
- **Cluster**: Node authentication, heartbeat timeout, leader re-election