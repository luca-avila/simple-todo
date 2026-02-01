# Project Overview

This is a solo-built Todo application.

Primary goals:
- Practice a vibe-coding workflow
- Build a clean, production-style monolith
- Learn by reading and refactoring AI-generated code
- Ship something deployable

Secondary goals:
- Keep scope small
- Avoid premature complexity
- Optimize for clarity over features

---

# Tech Stack (Decisions Locked)

- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy (async)
- Auth: JWT (access + refresh)
- Frontend: Vue (Vite)
- Infra: Docker, Nginx

---

# Architecture

- Monolithic backend
- Feature-based internal structure
- One database
- One deployment unit

No microservices.

---

# Initial Domain (Phase 1)

Entities:
- User
- Task

Rules:
- A task belongs to exactly one user
- Only the owner can read or modify their tasks
- Tasks can be marked as completed

Out of scope for now:
- Groups
- Permissions
- Sharing
- Roles
- Soft deletes

---

# Phases

## Phase 0 – Project Bootstrap
- Backend project scaffold
- Database connection
- Basic app configuration
- Health check endpoint

## Phase 1 – Authentication
- User registration
- Login
- JWT issuance
- Auth dependency

## Phase 2 – Personal Todos
- Task model
- CRUD endpoints
- Ownership enforcement

---

# Constraints

- Keep each phase reviewable in isolation
- No over-engineering
- Prefer clarity over abstractions
- Avoid adding features outside current phase

---

# Workflow Rules (Important)

- Work phase by phase
- One vertical slice at a time
- Claude implements only the current phase
- Changes must be readable in under 10 minutes
- Claude must NOT commit changes

---

# Output Expectations

For each phase:
- Implement only the scoped items
- Summarize changes
- List files modified
- Suggest a commit message