from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str | None = Field(None, exmaple="코딩 공부하기")

class Task(TaskBase):
    id: int
    done: bool = Field(False, description="완료 플래그")

    class Config:
        orm_mode = True

class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True