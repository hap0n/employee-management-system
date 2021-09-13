from datetime import date
from typing import List, Optional

from fastapi import APIRouter

from app.models.holiday_model import Holiday
from app.repositories.holiday_repository import HolidayRepository

holiday_router = APIRouter()


@holiday_router.get("/", response_model=List[Holiday], tags=["Holiday"])
async def get_list() -> List[Holiday]:
    holidays = await HolidayRepository.get_list()
    return holidays


@holiday_router.get("/{holiday_id}", response_model=Holiday, tags=["Holiday"])
async def get_holiday(holiday_id: int) -> Optional[Holiday]:
    holiday = await HolidayRepository.get_by_id(holiday_id)
    return holiday


@holiday_router.get("/between/", response_model=List[Holiday], tags=["Holiday"])
async def get_holidays_between(start_date: date, end_date: date) -> List[Holiday]:
    holidays = await HolidayRepository.between(start_date, end_date)
    return holidays


@holiday_router.put("/update", response_model=Holiday, tags=["Holiday"])
async def update_holiday(holiday: Holiday):
    holiday = await HolidayRepository.update(holiday)
    return holiday


@holiday_router.post("/create", response_model=Holiday, tags=["Holiday"])
async def create_holiday(holiday: Holiday):
    holiday = await HolidayRepository.save(holiday)
    return holiday


@holiday_router.delete("/delete/{holiday_id}", tags=["Holiday"])
async def delete_holiday(holiday_id: int) -> bool:
    response = await HolidayRepository.delete(holiday_id)
    return response
