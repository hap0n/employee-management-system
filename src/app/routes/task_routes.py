from typing import List, Optional

from fastapi import APIRouter

from app.models.task_model import Task
from app.repositories.task_repository import TaskRepository

task_router = APIRouter()


@task_router.get("/", response_model=List[Task], tags=["Task"])
async def get_list() -> List[Task]:
    tasks = await TaskRepository.get_list()
    return tasks


@task_router.get("/{task_id}", response_model=Task, tags=["Task"])
async def get_task(task_id: int) -> Optional[Task]:
    task = await TaskRepository.get_by_id(task_id)
    return task


@task_router.post("/update", response_model=Task, tags=["Task"])
async def update_task(task: Task):
    task = await TaskRepository.upsert(task)
    return task


@task_router.put("/create", response_model=Task, tags=["Task"])
async def create_task(task: Task):
    task = await TaskRepository.upsert(task)
    return task


@task_router.delete("/delete/{task_id}", tags=["Task"])
async def delete_task(task_id: int) -> bool:
    response = await TaskRepository.delete(task_id)
    return response
