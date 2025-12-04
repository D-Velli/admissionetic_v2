FROM python:3.13-slim

WORKDIR /app

# Libs système (psycopg, etc.)
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY . .

ENV PYTHONUNBUFFERED=1

# ⚠️ alembic.ini + dossier alembic doivent être à /app
# CMD ["bash", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]


# Script d'attente de la DB
COPY wait_for_db.sh /app/wait_for_db.sh
RUN chmod +x /app/wait_for_db.sh

CMD ["bash", "/app/wait_for_db.sh"]