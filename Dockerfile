# Multi-stage build keeps the final image small and free of build tooling.

# ---- Stage 1: build wheels for dependencies ----
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
# Pre-build dependency wheels so the final stage installs fast and offline.
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- Stage 2: minimal runtime image ----
FROM python:3.12-slim

# Run as a non-root user — a basic but expected security practice.
RUN useradd --create-home --uid 10001 appuser
WORKDIR /app

# Install deps from the pre-built wheels, then drop them.
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

COPY app/ ./app/

USER appuser

# Stamp a default; CI overrides this with the real version at build time.
ENV APP_VERSION=0.1.0
EXPOSE 8080

# Container-level healthcheck (Docker); Kubernetes will also probe /health.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8080/health').status==200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
