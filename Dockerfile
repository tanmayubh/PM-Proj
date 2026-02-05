FROM python:3.9-slim

# system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install Python deps first (Docker cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# expose FastAPI port
EXPOSE 8000

# make entrypoint executable
RUN chmod +x entrypoint.sh

# entrypoint handles Alembic + uvicorn
ENTRYPOINT ["./entrypoint.sh"]
