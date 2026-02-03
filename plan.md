# Production Readiness Plan

Improvements needed before deploying to VPS.

---

## 1. SSL/TLS with Nginx

- Configure HTTPS on the VPS nginx (outside Docker)
- Obtain certificates via Let's Encrypt / Certbot
- Proxy `https://yourdomain.com` → `http://localhost:3000` (frontend container)

## 2. Production Docker Compose Override

- **File:** `docker-compose.prod.yml`
- Remove development volumes (`./backend:/app`)
- Remove `--reload` from uvicorn command
- Set `DEBUG=false`
- Restrict exposed ports (no need to expose 8000 and 5432 externally)

## 3. Database Backups

- Set up periodic `pg_dump` via cron on the VPS
- Store backups off-server (S3, rsync, etc.)

## 4. Environment Security

- Use strong, unique `SECRET_KEY` per environment
- Don't commit `.env` to git (already in `.gitignore`)
- Change default PostgreSQL credentials for production

---

## Checklist

1. [ ] Set up VPS with nginx + certbot
2. [ ] Create `docker-compose.prod.yml`
3. [ ] Configure database backups
4. [ ] Harden environment variables
