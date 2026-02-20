from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.task as task_schema
import api.crud.task as task_crud
from api.db import get_db

router = APIRouter()

@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks_with_done(db)

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def list_tasks(
    task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
    ):
    return await task_crud.create_task(db, task_body)

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
    ):

    # task_id를 통해 조회
    original = await task_crud.get_task(db, task_id=task_id)

    # 없는 경우 예외처리
    if original is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # update 로직 실행 후 반환
    return await task_crud.update_task(db, task_body, original=original)
    

@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):

    original = await task_crud.get_task(db, task_id=task_id)

    if original is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return await task_crud.delete_task(db, original)