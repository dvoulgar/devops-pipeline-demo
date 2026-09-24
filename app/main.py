"""Minimal FastAPI service — the deploy target for the DevOps pipeline.

The app is intentionally boring: its job is to be something real to build,
containerize, ship through CI/CD, deploy to Kubernetes, and monitor.
"""
import os

from fastapi import FastAPI

# Version is read from an env var so the CI/CD pipeline can stamp each build
# (e.g. the git SHA or a semver tag) instead of hardcoding ":latest".
APP_VERSION = os.getenv("APP_VERSION", "0.1.0-dev")

app = FastAPI(title="devops-pipeline-demo", version=APP_VERSION)


@app.get("/")
def root():
    """Human-facing root endpoint."""
    return {"service": "devops-pipeline-demo", "version": APP_VERSION}


@app.get("/health")
def health():
    """Liveness/readiness probe target.

    Kubernetes probes and Prometheus/Grafana monitoring hit this.
    Keep it cheap and dependency-free so it reflects only 'is the process up'.
    """
    return {"status": "ok"}
