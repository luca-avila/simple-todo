# Frontend Short-Term Plan

Goal: Build a minimal Vue frontend for the existing backend.

---

## Scope

Three views:
- Login page
- Register page
- Task list page (authenticated)

---

## Steps

### 1. Project Setup
- Create Vue project with Vite
- Install axios for API calls
- Basic folder structure

### 2. Login Page
- Email + password form
- Call POST /api/v1/auth/login
- Store JWT token
- Redirect to task list on success
- Link to register page

### 3. Register Page
- Email + password form
- Call POST /api/v1/auth/register
- Redirect to login on success

### 4. Task List Page
- Fetch tasks from GET /api/v1/tasks
- Display tasks in a simple list
- Add new task form
- Mark task complete (checkbox)
- Delete task button

### 5. Auth Guard
- Redirect to login if no token
- Attach token to API requests

---

## Out of Scope
- Fancy styling
- State management (Pinia)
- Error toasts
- Loading spinners

---

## Current Step
Not started.
