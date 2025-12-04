#!/usr/bin/env bash
set -e

echo "🔍 Vérif des variables DB :"
echo "  DB_HOST=${DB_HOST}"
echo "  DB_PORT=${DB_PORT}"
echo "  DB_USER=${DB_USER}"
echo "  DB_NAME=${DB_NAME}"

if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ]; then
  echo "❌ DB_HOST ou DB_PORT non défini. Vérifie ton docker-compose."
  exit 1
fi

echo "⏳ Attente de la DB ${DB_HOST}:${DB_PORT}..."

# On teste juste si Postgres écoute, pas besoin de user / db
until pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; do
  echo "DB pas prête, on réessaie..."
  sleep 2
done

echo "✅ DB prête, on lance les migrations..."

alembic upgrade head

echo "🚀 Lancement de l'API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
