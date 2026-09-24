# devops-pipeline-demo

A minimal web service used as the deploy target for an end-to-end DevOps
pipeline. The application is intentionally simple — the portfolio value is in
the tooling around it: containerization, CI/CD, Infrastructure as Code, and
monitoring.

## Architecture (target state)

```
  Code (GitHub)
      │  push
      ▼
  CI/CD (build → test → scan → push image)   ← TODO
      │
      ▼
  Container registry (ECR)                    ← TODO
      │
      ▼
  Kubernetes (EKS), provisioned by Terraform  ← TODO
      │  Ingress
      ▼
  Users  ──►  /  ,  /health
      ▲
      │ scrape
  Prometheus + Grafana (monitoring)           ← TODO
```

## The app

| Endpoint  | Purpose                                             |
|-----------|-----------------------------------------------------|
| `GET /`       | Root — returns service name + version           |
| `GET /health` | Liveness/readiness probe + monitoring target    |

Version comes from the `APP_VERSION` env var so the pipeline can stamp each
build with a git SHA or semver tag instead of using `:latest`.

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

## Roadmap

- [x] Minimal service + `/health`
- [x] Containerized (multi-stage, non-root, healthcheck)
- [ ] CI/CD pipeline (build, test, Trivy scan, push to ECR)
- [ ] Terraform: VPC + EKS + ECR (remote state in S3)
- [ ] Deploy to EKS via Ingress
- [ ] Prometheus + Grafana dashboards and alerts
