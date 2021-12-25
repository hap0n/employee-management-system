from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TaskStatus(str, Enum):
    DONE = "done"
    IN_PROGRESS = "in_progress"
    SELECTED_FOR_DEVELOPMENT = "selected_for_development"


class TaskPriority(str, Enum):
    MINOR = "minor"
    NORMAL = "normal"
    MAJOR = "major"


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str]
    task_priority: TaskPriority
    task_status: TaskStatus
    assignee_id: int
    reporter_id: int
    created_at: datetime
    employee_id: int
