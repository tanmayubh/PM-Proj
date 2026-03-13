# Project Management Tool – Backend

Enterprise-grade backend API for project and task management with role-based access control.

## Tech Stack
- **FastAPI** - Modern async web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM with async support
- **Alembic** - Database migrations
- **JWT** - Token-based authentication
- **Docker & Docker Compose** - Containerization
- **Pydantic** - Data validation

## Features
✅ User authentication with JWT tokens
✅ Role-based access control (Admin, Manager, Member)
✅ Project management with timestamps
✅ Task assignment and status tracking
✅ Pagination support on list endpoints
✅ Global exception handling
✅ CORS enabled for frontend integration
✅ Comprehensive logging
✅ API documentation at `/docs`

## API Endpoints

### Authentication
- `POST /auth/login` - Login with credentials
- `POST /auth/register` - Register new user
- `GET /auth/me` - Get current user profile

### Projects
- `GET /projects` - List projects (paginated)
- `POST /projects` - Create project (admin/manager)
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project (admin/manager)
- `DELETE /projects/{id}` - Delete project (admin only)
- `GET /projects/{id}/tasks` - Get project tasks

### Tasks
- `GET /tasks` - List all tasks (admin/manager)
- `POST /tasks` - Create task
- `GET /tasks/{id}` - Get task details
- `PATCH /tasks/{id}` - Update task status
- `DELETE /tasks/{id}` - Delete task (admin/manager)
- `GET /tasks/user/{user_id}` - Get user's tasks

### Users
- `GET /users` - List users (admin/manager)
- `POST /users` - Create user (admin)
- `GET /users/{id}` - Get user details
- `PATCH /users/{id}/role` - Update user role (admin)
- `PATCH /users/{id}/deactivate` - Deactivate user (admin)
- `PATCH /users/{id}/activate` - Reactivate user (admin)

## Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Docker (optional)

### Local Development

1. **Clone repository**
```bash
git clone <repo-url>
cd PM_Proj
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
cp .env.example .env
# Edit .env with your database URL
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start development server**
```bash
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Docker Deployment

```bash
docker-compose up --build
```

## Environment Variables

```
DATABASE_URL=postgresql://user:password@localhost:5432/pm_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Authentication

All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <token>
```

Obtain token via `/auth/login` or `/auth/register`

## Role-Based Access

- **Admin**: Full access, manage users and projects
- **Manager**: Create/update projects, manage tasks
- **Member**: Create/update own tasks, view assigned tasks

## Development

### Run tests
```bash
pytest tests/ -v
```

### Code formatting
```bash
black .
flake8 .
```

## Database Schema

Users → Projects (1:N)
Users → Tasks (1:N)
Projects → Tasks (1:N)

## License

MIT