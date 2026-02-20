from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str | None = Field(None, exmaple="코딩 공부하기")
    done: bool = Field(False, description="완료 플래그")