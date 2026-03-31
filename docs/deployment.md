# Railway Deployment

## Setup

1. Create a new Railway project
2. Add PostgreSQL plugin
3. Add service from repo: `backend/` directory
   - Set env: `DATABASE_URL` (from PostgreSQL plugin), `NOKIA_MODE=mock`
4. Add service from repo: `frontend/` directory
5. Set up networking: frontend is public-facing, backend is internal

## Environment Variables (backend)

- `DATABASE_URL` — provided by Railway PostgreSQL
- `NOKIA_MODE` — `mock` or `real`
- `NOKIA_API_KEY` — when available
- `NOKIA_API_SECRET` — when available

## Notes

- Backend runs seed on startup automatically via FastAPI lifespan
- Frontend proxies /api and /ws to backend via nginx
- For Railway: update `frontend/nginx.conf` backend hostname to match Railway internal DNS
