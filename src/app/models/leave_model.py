from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class LeaveType(str, Enum):
    VACATION = "vacation"
    SICK_LEAVE = "sick_leave"


class LeaveStatus(str, Enum):
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    PENDING = "pending"


class Leave(BaseModel):
    id: Optional[int] = None
    leave_type: LeaveType
    start_date: date
    end_date: date
    leave_status: LeaveStatus
    approved_by: Optional[int]
    requested_at: datetime
    approved_at: Optional[datetime]
    employee_id: int
