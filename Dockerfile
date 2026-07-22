# AtherOS v1.0.0-rc1 — Production Dockerfile
# Multi-stage build: slim runtime image for the API server

# ──────────────────────────────────────────────────────────────────────────────
# Stage 1: Builder — install dependencies in an isolated layer
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /build

# Install build essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into /install prefix
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# ──────────────────────────────────────────────────────────────────────────────
# Stage 2: Runtime — minimal production image
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

LABEL maintainer="AtherOS Team"
LABEL version="1.0.0-rc1"
LABEL description="AtherOS AI Operating System — API Server"

# Create non-root user for security
RUN useradd -m -u 1000 atheros

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY backend/ ./backend/
COPY VERSION .
COPY .env.example .env.example

# Create required runtime directories
RUN mkdir -p logs backups plugins && \
    chown -R atheros:atheros /app

# Switch to non-root user
USER atheros

# Environment defaults (override at runtime)
ENV ATHEROS_ENV=production \
    API_HOST=0.0.0.0 \
    API_PORT=8000 \
    LOG_LEVEL=INFO \
    LOG_FORMAT=json \
    DATABASE_URL=sqlite:///./atheros.db \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

CMD ["python", "-m", "uvicorn", "backend.app.api.app:app", \
     "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
