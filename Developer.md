# Developer Documentation

This document explains how developers can run, test, and extend the Project Management API locally.

---

# Project Overview

This backend service provides a structured API for managing:

- Users
- Projects
- Tasks
- Authentication

The system follows an API-first architecture built with FastAPI and SQLAlchemy.

---

# Tech Stack

Backend Framework  
FastAPI

Language  
Python 3.9+

Database  
PostgreSQL (production)  
SQLite (development fallback)

ORM  
SQLAlchemy

Migrations  
Alembic

Authentication  
JWT tokens

Testing  
Pytest

Containerization  
Docker

CI/CD  
GitHub Actions

---

# Project Structure

```
project-root
│
├── app
│   ├── routers
│   ├── models
│   ├── schemas
│   ├── services
│   └── database.py
│
├── tests
├── alembic
├── docker
├── main.py
├── requirements.txt
└── DEVELOPER.md
```

---

# Running the Project Locally

## 1 Clone repository

```
git clone https://github.com/tanmayubh/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```

---

## 2 Install dependencies

```
pip install -r requirements.txt
```

---

## 3 Configure environment variables

Create a `.env` file or export variables manually.

Example:

```
DATABASE_URL=sqlite:///./test.db
JWT_SECRET_KEY=change_this_secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

SQLite is recommended for local development.

---

## 4 Run database migrations

```
alembic upgrade head
```

This creates the required database tables.

---

## 5 Start the API server

```
uvicorn main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates API documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

Developers can test API endpoints directly from the Swagger interface.

---

# Running Tests

Run the test suite using pytest.

```
pytest
```

---

# Running with Docker

Build the container:

```
docker build -t pm-api .
```

Run container:

```
docker run -p 8000:8000 pm-api
```

The API will be available at:

```
http://localhost:8000
```

---

# Continuous Integration

The repository includes a GitHub Actions workflow that runs automatically on:

- push
- pull_request

The CI pipeline performs:

- dependency installation
- test execution
- build validation

---

# Development Guidelines

When adding new features:

1. Define database model in `models`
2. Add request/response schema in `schemas`
3. Implement logic in `services`
4. Create endpoint in `routers`
5. Write tests in `tests`

---

# Future Improvements

- task lifecycle states
- role-based permissions
- event logging
- audit history
- notification service

---

# Maintainer

Tanmay Ubhate

GitHub  
https://github.com/tanmayubh
