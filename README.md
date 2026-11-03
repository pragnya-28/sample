# Kyma AI Resource Monitor

A Flask-based demo application for monitoring AI usage across different sources and estimating how much natural resources are consumed as a result of model usage, compute, and infrastructure demand.

## What this project demonstrates

- Flask REST API for operational dashboards
- Login and RBAC using session-based auth
- Audit logging for important actions
- Mock AI usage events from multiple sources
- Natural-resource impact estimation based on tokens, runtime, and power consumption
- Kubernetes/Kyma-friendly deployment model
- Helm chart with liveness and readiness probes
- GitHub Actions CI workflow

## Stack

- Python 3.11
- Flask
- Gunicorn
- PostgreSQL-ready data model patterns
- Docker
- Helm
- GitHub Actions
- pytest

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.main:app
flask run --host 0.0.0.0 --port 8080
```

## Demo login

The app includes mock users:

- ops-admin / admin123
- ai-analyst / analyst123
- viewer / viewer123

## API examples

```bash
curl -X POST http://localhost:8080/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username":"ops-admin","password":"admin123"}'

curl http://localhost:8080/api/v1/dashboard
curl http://localhost:8080/api/v1/usage
curl http://localhost:8080/api/v1/audits
```

## Docker

```bash
docker build -t kyma-ai-resource-monitor .
docker run --rm -p 8080:8080 kyma-ai-resource-monitor
```

## Render / Railway deployment

This app is also ready for a free public deployment while keeping the Kubernetes/Kyma story intact.

### Render

- Push the repo to GitHub
- Create a new Web Service on Render
- Use the repo and keep the default Python/Docker build settings
- Set the start command to:

```bash
gunicorn --bind 0.0.0.0:${PORT:-8080} app.main:app
```

### Railway

- Connect the GitHub repo
- Deploy as a Python or Docker app
- Keep the same gunicorn start command

## Helm deployment

```bash
helm install kyma-ai-resource-monitor ./helm/ai-resource-monitor
```

The chart includes:

- Deployment
- ClusterIP Service
- Liveness probe
- Readiness probe
- Kyma-style labels and metadata

## Tests

```bash
pytest -q
```

## Notes

- All data is mock-only and intended for demo purposes.
- This project was designed to match a real-world platform engineering and AI governance story for a Kubernetes/Kyma environment.
