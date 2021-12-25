from typing import List, Optional

from fastapi import APIRouter

from app.models.internal_position_model import InternalPosition
from app.models.position_model import Position, PositionType
from app.models.project_position_model import ProjectPosition
from app.repositories.internal_position_repository import InternalPositionRepository
from app.repositories.position_repository import PositionRepository
from app.repositories.project_position_repository import ProjectPositionRepository
from app.responces.position_response import (
    InternalPositionPathResponse,
    InternalPositionResponse,
    ProjectPositionPathResponse,
    ProjectPositionResponse,
)
from app.services.positions_service import PositionsService

position_router = APIRouter()


@position_router.get("/position/", response_model=List[Position], tags=["Positions"])
async def get_list() -> List[Position]:
    positions = await PositionRepository.get_list()
    return positions


@position_router.get("/internal-position/", response_model=List[InternalPosition], tags=["Positions"])
async def get_list() -> List[InternalPosition]:
    internal_positions = await InternalPositionRepository.get_list()
    return internal_positions


@position_router.get("/project-position/", response_model=List[ProjectPosition], tags=["Positions"])
async def get_list() -> List[ProjectPosition]:
    project_position = await ProjectPositionRepository.get_list()
    return project_position


@position_router.get("/position/{position_id}", response_model=Position, tags=["Positions"])
async def positions(position_id: int) -> Optional[Position]:
    position = await PositionRepository.get_by_id(position_id)
    return position


@position_router.post("/position/update", response_model=Position, tags=["Positions"])
async def update_position(position: Position):
    position = await PositionRepository.upsert(position)
    return position


@position_router.put("/position/create", tags=["Positions"])
async def create_position(position: Position):
    position = await PositionRepository.upsert(position)
    return position


@position_router.post("/project-position/update", response_model=Position, tags=["Positions"])
async def update_position(position: ProjectPosition):
    position = await ProjectPositionRepository.upsert(position)
    return position


@position_router.put("/project-position/create", tags=["Positions"])
async def create_position(position: ProjectPosition):
    position = await ProjectPositionRepository.upsert(position)
    return position


@position_router.post("/internal-position/update", response_model=Position, tags=["Positions"])
async def update_position(position: InternalPosition):
    position = await InternalPositionRepository.upsert(position)
    return position


@position_router.put("/internal-position/create", tags=["Positions"])
async def create_position(position: InternalPosition):
    position = await InternalPositionRepository.upsert(position)
    return position


@position_router.get(
    "/internal-position-path/{position_id}", response_model=InternalPositionPathResponse, tags=["Positions"]
)
async def get_path_to_root(position_id: int):
    path = PositionsService.get_path_to_root(position_id, PositionType.INTERNAL)
    return InternalPositionPathResponse(path=path)


@position_router.get(
    "/project-position-path/{position_id}", response_model=ProjectPositionPathResponse, tags=["Positions"]
)
async def get_path_to_root(position_id: int):
    path = PositionsService.get_path_to_root(position_id, PositionType.PROJECT)
    return ProjectPositionPathResponse(path=path)


@position_router.get("/internal-position/{position_id}", response_model=InternalPositionResponse, tags=["Positions"])
async def get_path_to_root(internal_position_id: int):
    internal_position = await InternalPositionRepository.get_by_id(internal_position_id)

    if internal_position:
        children = await InternalPositionRepository.get_children_positions(internal_position.id)
        parent = await InternalPositionRepository.get_by_id(internal_position.reporsts_to)
        position = await PositionRepository.get_by_id(internal_position.position_id)

        return InternalPositionResponse(id=internal_position_id, position=position, parent=parent, childern=children)


@position_router.get("/project-position/{position_id}", response_model=ProjectPositionResponse, tags=["Positions"])
async def get_path_to_root(internal_position_id: int):
    project_position = await ProjectPositionRepository.get_by_id(internal_position_id)

    if project_position:
        children = await ProjectPositionRepository.get_children_positions(project_position.id)
        parent = await ProjectPositionRepository.get_by_id(project_position.reporsts_to)
        position = await PositionRepository.get_by_id(project_position.position_id)

        return ProjectPositionResponse(id=internal_position_id, position=position, parent=parent, childern=children)
