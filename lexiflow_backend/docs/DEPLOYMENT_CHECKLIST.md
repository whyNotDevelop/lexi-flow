# Deployment Checklist – LexiFlow Backend

## Prerequisites
- Render.com account (free tier)
- GitHub repository with `main` branch
- Dockerfile in `lexiflow_backend/`

## One-Time Setup

### 1. Create PostgreSQL database on Render
- New → PostgreSQL → Free plan
- Name: `lexiflow-db`
- Copy the **Internal Database URL** after creation.

### 2. Set environment variables in Render web service

| Key | Value |
|-----|-------|
| `DJANGO_SETTINGS_MODULE` | `lexiflow_backend.settings.prod` |
| `DJANGO_SECRET_KEY` | Generate with: `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DJANGO_DEBUG` | `false` |
| `ALLOWED_HOSTS` | `.onrender.com,localhost` |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` |
| `DATABASE_URL` | (paste Internal Database URL from step 1) |
| `REDIS_HOST` | `localhost` (or leave blank – fallback to LocMemCache) |
| `REDIS_PORT` | `6379` |
| `DJANGO_SUPERUSER_EMAIL` | (your admin email) |
| `DJANGO_SUPERUSER_PASSWORD` | (strong password) |
| `DJANGO_SUPERUSER_FULL_NAME` | `Admin User` (optional) |

### 3. Deploy web service
- New → Web Service → Connect GitHub repo
- Root directory: `lexiflow_backend`
- Runtime: Docker (detected automatically)
- Plan: Free
- Click **Create Web Service**

---

## Deployment Process

- Push to `main` branch → Render automatically redeploys.
- Build steps (Docker): installs dependencies, collects static files.
- Startup command: runs migrations, creates superuser, starts gunicorn (as defined in Dockerfile CMD).

---

## Post-Deployment Verification

- Visit `https://lexiflow-backend.onrender.com/admin/` – should load with CSS.
- Log in with superuser credentials.
- Test lookup endpoint: `https://lexiflow-backend.onrender.com/api/words/lookup/hello/`
- Check logs in Render dashboard → Logs tab.

---

## Troubleshooting

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| DisallowedHost | `ALLOWED_HOSTS` missing Render domain | Add `.onrender.com` (with leading dot) |
| Static files 404 | WhiteNoise not configured or `collectstatic` not run | Ensure `STATICFILES_STORAGE` is set and Dockerfile runs `collectstatic` |
| Database connection error | `DATABASE_URL` not set or wrong | Copy Internal Database URL from Render PostgreSQL |
| Migrations not applied | Startup command missing `migrate` | Verify Dockerfile `CMD` includes `python manage.py migrate --noinput` |
| Superuser cannot log in | Environment variables not set or command not run | Check `DJANGO_SUPERUSER_*` vars; run `ensure_superuser` command manually via Render cron (if needed) |

---

## Rollback

- Render keeps previous deployments. Go to web service → **Deploy** tab → click **Rollback to previous deploy**.

---

## Useful Commands (local)

```bash
# Build Docker image locally
docker build -t lexiflow-backend .

# Run locally with production settings
docker run -p 8000:8000 --env-file .env.prod lexiflow-backend

# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(50))"
```