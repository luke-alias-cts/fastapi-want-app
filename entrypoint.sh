#!/bin/sh
set -e

# 데이터베이스가 준비될 때까지 대기 (선택 사항)
echo "Waiting for database at ${DB_HOST}:${DB_PORT}..."
while ! nc -z ${DB_HOST} ${DB_PORT}; do
  sleep 1
done

echo "Database is up, running migrations..."

# Alembic 마이그레이션 실행
uv run alembic upgrade head && \
echo "Starting application..." && \
exec uv run fastapi run app/main.py --port 8000 --host 0.0.0.0
