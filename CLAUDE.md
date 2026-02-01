# CLAUDE.md - AI Assistant Guide for simple-todo

## Project Overview

**simple-todo** is a production-oriented task manager application with group-based task management and role-based access control.

### Current Status
This project is in the **initial planning stage** - the repository has been initialized with architectural intent documented but no implementation yet.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy (recommended)

### Frontend
- **Framework**: Vue.js
- **State Management**: Pinia (recommended for Vue 3)
- **HTTP Client**: Axios or native fetch

### Infrastructure
- **Containerization**: Docker
- **Reverse Proxy**: Nginx
- **SSL/TLS**: HTTPS enabled

## Planned Project Structure

When implemented, the project should follow this structure:

```
simple-todo/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py            # Configuration and environment variables
│   │   ├── database.py          # Database connection and session management
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── group.py
│   │   │   └── task.py
│   │   ├── schemas/             # Pydantic schemas for request/response validation
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── group.py
│   │   │   └── task.py
│   │   ├── routers/             # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── groups.py
│   │   │   └── tasks.py
│   │   ├── services/            # Business logic layer
│   │   │   └── ...
│   │   └── utils/               # Utility functions
│   │       └── security.py      # JWT handling, password hashing
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Pytest fixtures
│   │   └── ...
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/                 # Database migrations
│       └── ...
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/              # Pinia stores
│   │   ├── router/
│   │   └── api/                 # API client modules
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── nginx/
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
└── CLAUDE.md
```

## Core Features to Implement

### Authentication System
- User registration with email/password
- JWT-based login/logout
- Token refresh mechanism
- Password hashing with bcrypt

### Group Management
- Create/read/update/delete groups
- Two roles: **owner** and **member**
- Owners can manage group membership and settings
- Members can view and interact with group tasks

### Task Management
- CRUD operations for tasks within groups
- Task assignment to group members
- Task status tracking (e.g., pending, in_progress, completed)
- Due dates and priorities

## Development Conventions

### Backend (Python/FastAPI)

#### Code Style
- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Use async/await for database operations

#### API Design
- Use RESTful conventions
- Prefix all API routes with `/api/v1/`
- Return appropriate HTTP status codes
- Use Pydantic models for request/response validation

#### Example Router Pattern
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.models.task import Task

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Implementation
    pass
```

#### Database Patterns
- Use SQLAlchemy ORM for database interactions
- Use Alembic for database migrations
- Never commit database credentials to version control

### Frontend (Vue.js)

#### Code Style
- Use Vue 3 Composition API with `<script setup>`
- Use single-file components (.vue)
- Follow Vue style guide recommendations

#### Component Naming
- Use PascalCase for component files (e.g., `TaskList.vue`)
- Use kebab-case in templates (e.g., `<task-list>`)

#### State Management
- Use Pinia for global state
- Keep component-local state when appropriate

### Testing

#### Backend Tests
- Use pytest for testing
- Maintain test fixtures in `conftest.py`
- Test API endpoints with FastAPI's TestClient
- Aim for high coverage on business logic

#### Frontend Tests
- Use Vitest for unit tests
- Use Vue Test Utils for component testing

### Docker

#### Development
```bash
docker-compose up --build
```

#### Environment Variables
- Use `.env` files for local development
- Never commit `.env` files (add to `.gitignore`)
- Provide `.env.example` as a template

## Common Commands

### Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Run migrations
alembic upgrade head
```

### Frontend
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test
```

### Docker
```bash
# Build and start all services
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f
```

## Security Considerations

- Store passwords using bcrypt hashing
- Use environment variables for secrets
- Implement rate limiting on authentication endpoints
- Validate and sanitize all user inputs
- Use HTTPS in production
- Implement CORS properly for the frontend origin
- Set secure cookie flags for JWT tokens stored in cookies

## Git Workflow

- Create feature branches from main
- Use descriptive commit messages
- Keep commits focused and atomic
- Run tests before pushing

## Notes for AI Assistants

1. **Start Small**: When implementing features, start with the minimal viable implementation and iterate
2. **Test-Driven**: Write tests alongside new features
3. **Security First**: Always consider security implications, especially for auth-related code
4. **Type Safety**: Use type hints in Python and TypeScript in Vue when possible
5. **Documentation**: Update this file when adding new patterns or conventions
6. **Environment**: Never hardcode secrets or environment-specific values
