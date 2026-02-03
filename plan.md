# Docker Setup Completion Plan

Goal: Make `docker compose up` fully functional for the entire stack.

---

## Current State

- ✅ `docker-compose.yml` exists with `db` and `backend` services
- ✅ `backend/Dockerfile` exists
- ✅ `.env.example` exists
- ❌ Frontend is not containerized
- ❌ No reverse proxy configuration
- ✅ CORS not needed (nginx proxies API requests, same-origin)
- ✅ `.env` file created

---

## Phase 1: Environment Configuration

### 1.1 Create .env file
- Copy `.env.example` to `.env`
- Update `SECRET_KEY` to a secure random value
- Ensure `DATABASE_URL` uses the Docker service name (`db`) instead of `localhost`

---

## Phase 2: Frontend Containerization

### 2.1 Create frontend Dockerfile
- **File:** `frontend/Dockerfile`
- Multi-stage build:
  - **Stage 1 (build):** Node.js image to run `npm install` and `npm run build`
  - **Stage 2 (serve):** Nginx Alpine to serve the built static files
- Copy built files from stage 1 to nginx html directory

### 2.2 Create nginx config for frontend
- **File:** `frontend/nginx.conf`
- Serve static files from `/usr/share/nginx/html`
- Handle SPA routing (fallback to `index.html` for Vue Router)
- Proxy `/api` requests to the backend service

### 2.3 Verify frontend API configuration
- **File:** `frontend/src/api/index.js`
- Ensure `baseURL` works in both development and production
- Use relative `/api/v1` path (nginx will proxy to backend)

---

## Phase 3: Docker Compose Updates

### 3.1 Add frontend service
- **File:** `docker-compose.yml`
- Add `frontend` service:
  - Build from `./frontend`
  - Expose port 80 (or 3000)
  - Depends on `backend`

### 3.2 Update service dependencies
- Ensure proper startup order: `db` → `backend` → `frontend`
- Add healthchecks for `db` and `backend` services

### 3.3 Configure networking
- All services on same Docker network (default)
- Frontend nginx proxies to `backend:8000`
- Backend connects to `db:5432`

---

## Phase 4: Production Readiness (Optional)

### 4.1 Add dedicated nginx reverse proxy
- Single entry point for the application
- SSL/TLS termination (with certificates)

### 4.2 Add healthcheck endpoints
- Backend: Add `/health` endpoint
- Database: Use pg_isready

### 4.3 Add production docker-compose override
- **File:** `docker-compose.prod.yml`
- Remove development volumes
- Set `DEBUG=false`
- Configure resource limits

---

## Implementation Checklist

1. [x] Phase 1.1 - Create .env file
2. [x] Phase 2.1 - Create frontend Dockerfile
3. [ ] Phase 2.2 - Create frontend nginx.conf
4. [ ] Phase 2.3 - Verify frontend API configuration
5. [ ] Phase 3.1 - Add frontend service to docker-compose.yml
6. [ ] Phase 3.2 - Add healthchecks
7. [ ] Test with `docker compose up --build`

---

## Expected Final Structure

```
simple-todo/
├── docker-compose.yml          # Updated with frontend service
├── .env                        # Created from .env.example
├── .env.example
├── backend/
│   └── Dockerfile              # Existing
└── frontend/
    ├── Dockerfile              # NEW
    ├── nginx.conf              # NEW
    └── src/
        └── api/
            └── index.js        # Verified/updated
```

---

## Verification Steps

After implementation, verify with:

```bash
# Build and start all services
docker compose up --build

# Check all containers are running
docker compose ps

# Test backend API
curl http://localhost:8000/api/v1/

# Test frontend (served by nginx)
curl http://localhost:3000

# Full flow test:
# 1. Open http://localhost:3000 in browser
# 2. Register a new user
# 3. Login
# 4. Create/edit/delete tasks
```
