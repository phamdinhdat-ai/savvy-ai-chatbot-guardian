
# SavvyAI Guardian: Advanced AI Chatbot Deployment Guide

This document provides instructions for deploying the SavvyAI Guardian chatbot to a Kubernetes cluster.

## Prerequisites

- Docker installed locally
- Access to a Kubernetes cluster
- kubectl CLI configured
- Python 3.11+

## Directory Structure

```
.
├── Dockerfile            # Container definition
├── requirements.txt      # Python dependencies
├── kubernetes/           # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── python/               # Python application code
    └── app/
        ├── main.py       # FastAPI application
        ├── rag.py        # RAG implementation
        ├── guardrails.py # Safety guardrails
        └── models.py     # LLM interface
```

## Deployment Steps

### 1. Build the Docker image

```bash
docker build -t savvy-ai-chatbot:latest .
```

### 2. Push to your container registry

```bash
docker tag savvy-ai-chatbot:latest your-registry/savvy-ai-chatbot:latest
docker push your-registry/savvy-ai-chatbot:latest
```

### 3. Update Kubernetes manifests

Edit `kubernetes/deployment.yaml` to use your container registry:

```yaml
image: your-registry/savvy-ai-chatbot:latest
```

### 4. Deploy to Kubernetes

```bash
kubectl apply -f kubernetes/
```

### 5. Verify deployment

```bash
kubectl get pods -l app=savvy-ai-chatbot
kubectl get services -l app=savvy-ai-chatbot
kubectl get ingress savvy-ai-chatbot-ingress
```

## Environment Variables

Configure the following environment variables:

- `OPENAI_API_KEY`: API key for OpenAI (if using OpenAI models)
- `ENVIRONMENT`: Set to "production", "staging", or "development"
- `LOG_LEVEL`: Set to "debug", "info", "warning", or "error"

## Scaling

The application can be scaled horizontally by adjusting the replica count:

```bash
kubectl scale deployment savvy-ai-chatbot --replicas=5
```

## Monitoring

Set up monitoring with Prometheus and Grafana:

```bash
# Add Prometheus annotations to the deployment.yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/path: "/metrics"
  prometheus.io/port: "8000"
```

## Troubleshooting

Common issues and solutions:

- **Pod not starting**: Check logs with `kubectl logs <pod-name>`
- **Service unavailable**: Verify service with `kubectl describe service savvy-ai-chatbot`
- **Authentication errors**: Check environment variables and secrets
