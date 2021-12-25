from typing import List, Optional

from fastapi import APIRouter

from app.models.team_model import Team, TeamStatus
from app.repositories.documnet_team_repository import DocumentTeamRepository
from app.repositories.employee_team_repository import EmployeeTeamRepository
from app.repositories.team_repository import TeamRepository
from app.responces.team_response import TeamResponse

team_router = APIRouter()


@team_router.get("/", response_model=List[Team], tags=["Team"])
async def get_list() -> List[Team]:
    teams = await TeamRepository.get_list()
    return teams


@team_router.get("/{team_id}", response_model=TeamResponse, tags=["Team"])
async def get_team(team_id: int) -> Optional[TeamResponse]:
    team = await TeamRepository.get_by_id(team_id)
    document_ids = await DocumentTeamRepository.get_team_docs(team_id)
    employee_ids = await EmployeeTeamRepository.get_team_employees(team_id)
    response = TeamResponse(
        id=team.id,
        status=team.status,
        name=team.name,
        lead_id=team.lead_id,
        division_id=team.division_id,
        employee_ids=document_ids,
        document_ids=employee_ids,
    )
    return response


@team_router.get("/search/", response_model=List[Team], tags=["Team"])
async def search_teams(
    limit: Optional[int], offset: Optional[int], name_prefix: Optional[str], status: Optional[TeamStatus],
) -> List[Team]:
    teams = await TeamRepository.index(limit=limit, offset=offset, name_prefix=name_prefix, status=status)
    return teams


@team_router.post("/update", response_model=Team, tags=["Team"])
async def update_position(team: Team):
    team = await TeamRepository.upsert(team)
    return team


@team_router.put("/create", response_model=Team, tags=["Team"])
async def create_position(team: Team):
    team = await TeamRepository.upsert(team)
    return team
