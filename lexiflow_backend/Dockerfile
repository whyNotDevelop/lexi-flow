# Dockerfile (production)
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the rest of the application
COPY . .

# Set the Django settings module to production
ENV DJANGO_SETTINGS_MODULE=lexiflow_backend.settings.prod

# Provide a dummy secret key for static collection (will be replaced at runtime)
ENV DJANGO_SECRET_KEY=dummy-secret-key-for-collectstatic-only

# Collect static files (requires the above env var)
RUN python manage.py collectstatic --noinput

# Run gunicorn (development server is not used)
CMD sh -c "python manage.py migrate --noinput && gunicorn lexiflow_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2"