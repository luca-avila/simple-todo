from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    owner_id: int

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    skip: int
    limit: int
