from pydantic import BaseModel, Field, ConfigDict

class TaskBase(BaseModel):
    title: str | None = Field(
    default=None,
    json_schema_extra={"example": "코딩 공부하기"},
)

class Task(TaskBase):
    id: int
    done: bool = Field(False, description="완료 플래그")

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
