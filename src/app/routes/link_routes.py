from typing import List, Optional

from fastapi import APIRouter

from app.models.link_model import Link
from app.repositories.link_repository import LinkRepository

link_router = APIRouter()


@link_router.get("/", response_model=List[Link], tags=["Link"])
async def get_list() -> List[Link]:
    links = await LinkRepository.get_list()
    return links


@link_router.get("/{link_id}", response_model=Link, tags=["Link"])
async def get_link(link_id: int) -> Optional[Link]:
    link = await LinkRepository.get_by_id(link_id)
    return link


@link_router.post("/update", response_model=Link, tags=["Link"])
async def update_link(link: Link):
    link = await LinkRepository.upsert(link)
    return link


@link_router.put("/create", response_model=Link, tags=["Link"])
async def create_link(link: Link):
    link = await LinkRepository.upsert(link)
    return link


@link_router.delete("/delete/{link_id}", tags=["Link"])
async def delete_link(link_id: int) -> bool:
    response = await LinkRepository.delete(link_id)
    return response
