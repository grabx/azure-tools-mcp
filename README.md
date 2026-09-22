# Azure Tools MCP Server

A lightweight [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server built with [FastMCP](https://github.com/jlowin/fastmcp) that exposes Azure helper tools to AI agents.

## Tools

| Tool | Description |
| --- | --- |
| `azure_sub_to_tenant` | Looks up Azure tenant details from an Azure subscription ID (UUID). |

The server also exposes a `GET /health` endpoint used for Kubernetes readiness/liveness probes.

## Getting started

### Run locally

```bash
pip install -r requirements.txt
fastmcp run main.py:mcp --transport http --host 0.0.0.0 --port 8000
```

### Run with Docker

```bash
docker build -t azure-tools-mcp .
docker run --rm -p 8000:8000 azure-tools-mcp
```

## Deployment

`manifest.yaml` contains a Kubernetes `Deployment` and `Service`. Update the image reference before applying:

```bash
kubectl apply -f manifest.yaml
```

## CI

`.github/workflows/build.yaml` builds a multi-architecture (`amd64`, `arm64`) Docker image on every push to `main` and pushes it to GitHub Container Registry (GHCR).

## Project layout

| File | Purpose |
| --- | --- |
| `main.py` | FastMCP server, MCP tools, and health route. |
| `Dockerfile` | Python 3.12 image running as a non-root user on port 8000. |
| `manifest.yaml` | Kubernetes `Deployment` + `Service` manifests. |
| `requirements.txt` | Runtime dependencies (`fastmcp`, `httpx`). |

## Notes

- The lookup is delegated to the external `sub2tenant.com` API.
