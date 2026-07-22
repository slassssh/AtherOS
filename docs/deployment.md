# AtherOS v1.0.0-rc1 — Deployment Guide

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone repo
git clone https://github.com/slassssh/AtherOS
cd AtherOS

# 2. Configure environment
cp .env.example .env
# Edit .env: set SECRET_KEY, LLM_API_KEY, etc.

# 3. Launch
docker-compose up -d

# 4. Verify
curl http://localhost:8000/api/v1/health
```

### Option 2: Direct Python

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env as needed

# Start API server
uvicorn backend.app.api.app:app --host 0.0.0.0 --port 8000 --reload

# Start Desktop (separate terminal)
python desktop/app/main.py
```

---

## Environment Profiles

| Profile | `ATHEROS_ENV` | `DEBUG` | `LOG_FORMAT` | `API_WORKERS` |
|---------|--------------|---------|--------------|---------------|
| Development | `development` | `True` | `text` | 1 |
| Testing | `testing` | `True` | `text` | 1 |
| Production | `production` | `False` | `json` | 4 |

---

## Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ Production | Strong random secret (min 32 chars) |
| `ATHEROS_ENV` | ✅ | `development` / `testing` / `production` |
| `DATABASE_URL` | Optional | Defaults to `sqlite:///./atheros.db` |
| `LLM_PROVIDER` | Optional | `mock` / `openai` / `ollama` / etc. |
| `LLM_API_KEY` | Provider-specific | OpenAI / Anthropic / OpenRouter key |

---

## Docker

```bash
# Build image
docker build -t atheros:1.0.0-rc1 .

# Run standalone
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY=your_secret_here \
  -e ATHEROS_ENV=production \
  -v atheros-data:/app/data \
  atheros:1.0.0-rc1

# Docker Compose
docker-compose up -d
docker-compose logs -f atheros-api
docker-compose down
```

---

## Health Endpoints

```bash
# Basic health
GET /api/v1/health
# → {"status": "healthy", "version": "1.0.0-rc1"}

# Detailed diagnostics
GET /api/v1/health/detailed
# → HealthReport with CPU/RAM/disk/DB/plugins/models/agents/cluster
```

---

## Backup & Restore

```bash
# Trigger backup via API
curl -X POST http://localhost:8000/api/v1/backups \
  -H "Content-Type: application/json" \
  -d '{"label": "pre-upgrade"}'

# List backups
curl http://localhost:8000/api/v1/backups

# Restore backup
curl -X POST http://localhost:8000/api/v1/backups/{backup_id}/restore
```

---

## Windows Executable

```bat
# Build .exe
scripts\build_windows.bat

# Run
dist\atheros-api.exe
```

## Linux Binary

```bash
# Build binary
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh

# Run
./dist/atheros-api
```
