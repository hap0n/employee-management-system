from typing import List, Optional

from fastapi import APIRouter

from app.models.leave_model import Leave
from app.repositories.leave_repository import LeaveRepository

leave_router = APIRouter()


@leave_router.get("/", response_model=List[Leave], tags=["Leave"])
async def get_list() -> List[Leave]:
    leaves = await LeaveRepository.get_list()
    return leaves


@leave_router.get("/{leave_id}", response_model=Leave, tags=["Leave"])
async def get_leave(leave_id: int) -> Optional[Leave]:
    leave = await LeaveRepository.get_by_id(leave_id)
    return leave


@leave_router.post("/update", response_model=Leave, tags=["Leave"])
async def update_leave(leave: Leave):
    leave = await LeaveRepository.upsert(leave)
    return leave


@leave_router.put("/create", response_model=Leave, tags=["Leave"])
async def create_leave(leave: Leave):
    leave = await LeaveRepository.upsert(leave)
    return leave


@leave_router.delete("/delete/{leave_id}", tags=["Leave"])
async def delete_leave(leave_id: int) -> bool:
    response = await LeaveRepository.delete(leave_id)
    return response
