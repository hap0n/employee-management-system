from typing import List, Optional

from fastapi import APIRouter

from app.models.division_model import Division, DivisionStatus
from app.repositories.division_repository import DivisionRepository
from app.repositories.document_division_repository import DocumentDivisionRepository
from app.repositories.team_division_repository import TeamDivisionRepository
from app.responces.division_response import DivisionResponse

division_router = APIRouter()


@division_router.get("/position/", response_model=List[Division], tags=["Positions"])
async def get_list() -> List[Division]:
    divisions = await DivisionRepository.get_list()
    return divisions


@division_router.get("/{division_id}", response_model=DivisionResponse, tags=["Division"])
async def get_division(division_id: int) -> Optional[DivisionResponse]:
    division = await DivisionRepository.get_by_id(division_id)
    document_ids = await DocumentDivisionRepository.get_division_docs(division_id)
    teams = await TeamDivisionRepository.get_division_teams(division_id)
    response = DivisionResponse(
        id=division.id,
        status=division.status,
        name=division.name,
        lead_id=division.lead_id,
        teams=teams,
        document_ids=document_ids,
    )
    return response


@division_router.get("/search/", response_model=Division, tags=["Division"])
async def search_divisions(
    limit: Optional[int], offset: Optional[int], name_prefix: Optional[str], status: Optional[DivisionStatus],
) -> List[Division]:
    divisions = await DivisionRepository.index(limit=limit, offset=offset, name_prefix=name_prefix, status=status)
    return divisions


@division_router.put("/update", response_model=Division, tags=["Division"])
async def update_position(division: Division):
    division = await DivisionRepository.update(division)
    return division


@division_router.post("/create", response_model=Division, tags=["Division"])
async def create_position(division: Division):
    division = await DivisionRepository.save(division)
    return division
