from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.crud.done as done_crud
import api.schemas.done as done_schema
from api.db import get_db

router = APIRouter()

@router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):

    # task_id를 통해 조회
    original = await done_crud.get_done(db, task_id=task_id)

    # 있는 경우 예외 처리
    if original is not None:
        raise HTTPException(status_code=400, detail="Done already exists")

    # done 생성 후 반환
    return await done_crud.create_done(db, task_id)

@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):

    original = await done_crud.get_done(db, task_id=task_id)

    if original is None:
        raise HTTPException(status_code=404, detail="Done task not found")
    
    return await done_crud.delete_done(db, original)