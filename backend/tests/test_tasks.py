import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User

pytestmark = pytest.mark.asyncio


async def test_create_task(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/v1/tasks/",
        headers=auth_headers,
        json={"title": "Test task", "description": "A test"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "A test"
    assert data["completed"] is False


async def test_create_task_minimal(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/v1/tasks/",
        headers=auth_headers,
        json={"title": "Just a title"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Just a title"
    assert data["description"] is None


async def test_create_task_unauthenticated(client: AsyncClient):
    response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Test task"},
    )
    assert response.status_code == 403


async def test_list_tasks_empty(client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


async def test_list_tasks(client: AsyncClient, auth_headers, test_user, db: AsyncSession):
    task1 = Task(title="Task 1", owner_id=test_user.id)
    task2 = Task(title="Task 2", owner_id=test_user.id)
    db.add_all([task1, task2])
    await db.commit()

    response = await client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 2
    titles = {t["title"] for t in data["items"]}
    assert titles == {"Task 1", "Task 2"}


async def test_list_tasks_pagination(
    client: AsyncClient,
    auth_headers,
    test_user,
    db: AsyncSession,
):
    for i in range(5):
        db.add(Task(title=f"Task {i}", owner_id=test_user.id))
    await db.commit()

    response = await client.get("/api/v1/tasks/?skip=2&limit=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["skip"] == 2
    assert data["limit"] == 2


async def test_list_tasks_only_own(
    client: AsyncClient,
    auth_headers,
    test_user,
    other_user,
    db: AsyncSession,
):
    my_task = Task(title="My task", owner_id=test_user.id)
    other_task = Task(title="Other task", owner_id=other_user.id)
    db.add_all([my_task, other_task])
    await db.commit()

    response = await client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "My task"


async def test_get_task(client: AsyncClient, auth_headers, test_user, db: AsyncSession):
    task = Task(title="Test task", owner_id=test_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    response = await client.get(f"/api/v1/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test task"


async def test_get_task_not_found(client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/tasks/9999", headers=auth_headers)
    assert response.status_code == 404


async def test_get_task_other_user(
    client: AsyncClient,
    auth_headers,
    other_user,
    db: AsyncSession,
):
    task = Task(title="Other's task", owner_id=other_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    response = await client.get(f"/api/v1/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404


async def test_update_task(client: AsyncClient, auth_headers, test_user, db: AsyncSession):
    task = Task(title="Original", owner_id=test_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    response = await client.patch(
        f"/api/v1/tasks/{task.id}",
        headers=auth_headers,
        json={"title": "Updated", "completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True


async def test_update_task_partial(
    client: AsyncClient,
    auth_headers,
    test_user,
    db: AsyncSession,
):
    task = Task(title="Original", description="Keep this", owner_id=test_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    response = await client.patch(
        f"/api/v1/tasks/{task.id}",
        headers=auth_headers,
        json={"completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Original"
    assert data["description"] == "Keep this"
    assert data["completed"] is True


async def test_update_task_other_user(
    client: AsyncClient,
    auth_headers,
    other_user,
    db: AsyncSession,
):
    task = Task(title="Other's task", owner_id=other_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    response = await client.patch(
        f"/api/v1/tasks/{task.id}",
        headers=auth_headers,
        json={"title": "Hacked"},
    )
    assert response.status_code == 404


async def test_delete_task(client: AsyncClient, auth_headers, test_user, db: AsyncSession):
    task = Task(title="To delete", owner_id=test_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    response = await client.delete(f"/api/v1/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 204

    response = await client.get(f"/api/v1/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404


async def test_delete_task_other_user(
    client: AsyncClient,
    auth_headers,
    other_user,
    db: AsyncSession,
):
    task = Task(title="Other's task", owner_id=other_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    response = await client.delete(f"/api/v1/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == 404
