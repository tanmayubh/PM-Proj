#!/bin/sh

echo "🚀 Waiting for DB..."
sleep 5

echo "📦 Running Alembic migrations..."
alembic upgrade head

echo "🔥 Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
