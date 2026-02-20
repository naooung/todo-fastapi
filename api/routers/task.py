from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.crud.task as task_crud
from api.db import get_db

import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tasks(db: Session = Depends(get_db)):
    return task_crud.get_tasks_with_done(db)

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task: task_schema.TaskCreate, db: Session = Depends(get_db)):
    return task_crud.create_task(db, task)

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task.model_dump())

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return