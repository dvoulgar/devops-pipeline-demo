# devops-pipeline-demo

[![CI](https://github.com/dvoulgar/devops-pipeline-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/dvoulgar/devops-pipeline-demo/actions/workflows/ci.yml)

**Status:** ✅ Phase 2 complete — CI pipeline green (tests → Docker build → Trivy scan) on every push.

An end-to-end DevOps pipeline built in deliberate phases: a minimal web service
taken from source all the way to a monitored deployment on Kubernetes. The
application is intentionally simple — the engineering value is in the tooling
around it: containerization, CI/CD, Infrastructure as Code, and observability.

## Target architecture

```
  Code (GitHub)
      │  push
      ▼
  CI/CD  (build → test → scan → push image)
      │
      ▼
  Container registry (ECR)
      │
      ▼
  Kubernetes (EKS), provisioned by Terraform
      │  Ingress
      ▼
  Users  ──►  /  ,  /health
      ▲
      │ scrape
  Prometheus + Grafana (monitoring)
```

## The app

| Endpoint      | Purpose                                      |
|---------------|----------------------------------------------|
| `GET /`       | Root — returns service name + version        |
| `GET /health` | Liveness/readiness probe + monitoring target |

Version comes from the `APP_VERSION` env var so the pipeline can stamp each
build with a git SHA or semver tag instead of using `:latest`.

The container image is a multi-stage build, runs as a non-root user, and
includes a healthcheck.

## Run locally (no Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
# then: curl localhost:8080/health
```

## Run in Docker

```bash
docker build -t devops-pipeline-demo:0.1.0 .
docker run -p 8080:8080 devops-pipeline-demo:0.1.0
curl localhost:8080/health   # -> {"status":"ok"}
```

## Build phases

The project is delivered in phases, each building on the last:

- **Phase 1 — Service & container** ✅ *(complete)*
  Minimal FastAPI service with `/health`, multi-stage non-root Dockerfile.
- **Phase 2 — CI** ✅ *(complete)*
  GitHub Actions on every push: run tests → build image → Trivy vulnerability scan.
  Image tagged by commit SHA; build gated on tests passing.
- **Phase 3 — Infrastructure as Code** *(next)*
  Terraform: VPC + EKS + ECR, remote state in S3.
- **Phase 4 — Deploy to Kubernetes**
  Kubernetes manifests + Ingress, probes wired to `/health`.
- **Phase 5 — Observability**
  Prometheus + Grafana dashboards and alerting.
