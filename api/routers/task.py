from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.crud.task as task_crud
from api.db import get_db

import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tasks(db: Session = Depends(get_db)):
    return task_crud.get_tasks_with_done(db)

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, db: Session = Depends(get_db)):
    return task_crud.create_task(db, task_body)

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate, db: Session = Depends(get_db)):

    # task_id를 통해 조회해서 task에 저장
    original = task_crud.get_task(db, task_id=task_id)

    # 없는 경우 예외처리
    if original is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # update 로직 실행 후 반환
    return task_crud.update_task(db, task_body, original=original)
    

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    return