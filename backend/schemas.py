from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCreateRequest(BaseModel):
    text: str


class TaskResponse(BaseModel):
    id: int
    task_name: str
    subject: Optional[str]
    deadline: datetime
    difficulty: int
    urgency_score: float
    priority_score: float
    priority_label: str
    created_at: datetime

    class Config:
        from_attributes = True


class ScheduleResponse(BaseModel):
    schedule: str