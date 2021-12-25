from typing import List, Optional

from fastapi import APIRouter

from app.models.phone_model import Phone
from app.repositories.phone_repository import PhoneRepository

phone_router = APIRouter()


@phone_router.get("/", response_model=List[Phone], tags=["Phone"])
async def get_list() -> List[Phone]:
    phones = await PhoneRepository.get_list()
    return phones


@phone_router.get("/{phone_id}", response_model=Phone, tags=["Phone"])
async def get_phone(phone_id: int) -> Optional[Phone]:
    phone = await PhoneRepository.get_by_id(phone_id)
    return phone


@phone_router.post("/update", response_model=Phone, tags=["Phone"])
async def update_phone(phone: Phone):
    phone = await PhoneRepository.upsert(phone)
    return phone


@phone_router.put("/create", response_model=Phone, tags=["Phone"])
async def create_phone(phone: Phone):
    phone = await PhoneRepository.upsert(phone)
    return phone


@phone_router.delete("/delete/{phone_id}", tags=["Phone"])
async def delete_phone(phone_id: int) -> bool:
    response = await PhoneRepository.delete(phone_id)
    return response
