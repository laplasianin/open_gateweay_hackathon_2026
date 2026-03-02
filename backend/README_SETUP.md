# StageFlow Backend

FastAPI-based backend server for the StageFlow event management platform.

## Features

- **FastAPI Framework**: Modern async Python web framework
- **Structured Logging**: Using structlog for JSON-formatted logs
- **PostgreSQL Database**: Docker-based PostgreSQL for data persistence
- **Nokia Network as Code Integration**: Ready for telecom network APIs
- **Pydantic Models**: Type-safe request/response validation

## Prerequisites

- Python 3.14+
- uv (package manager)
- Docker & Docker Compose (for PostgreSQL)

## Setup

### 1. Install Dependencies

```bash
cd backend
uv sync
```

### 2. Start PostgreSQL

```bash
docker-compose up -d
```

### 3. Configure Environment

Edit `.env` file with your settings:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/stageflow
NAC_CLIENT_ID=your_client_id
NAC_CLIENT_SECRET=your_client_secret
```

### 4. Run Server

```bash
.venv/bin/python main.py
```

Server will start at `http://localhost:8000`

## API Endpoints

### Health Check

```bash
GET /healthcheck
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-03-02T13:44:23.764122",
  "database": "connected"
}
```

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── app.py              # FastAPI application factory
│   ├── config.py           # Configuration management
│   ├── logging_config.py   # Structlog configuration
│   └── models.py           # Pydantic models
├── main.py                 # Application entry point
├── docker-compose.yml      # PostgreSQL setup
├── .env                    # Environment variables
└── pyproject.toml          # Project metadata
```

## Development

Logs are output in JSON format via structlog.

## Deployment

Future: Google Cloud SQL integration

