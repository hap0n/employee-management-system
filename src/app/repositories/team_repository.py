from typing import List, Optional

from pypika import Table
from pypika.enums import Dialects
from pypika.functions import Lower
from pypika.queries import QueryBuilder

from app.models.team_model import Team, TeamStatus
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class TeamRepository(BaseRepository):
    ENTITY = Team

    TABLE_NAME = "teams"
    TABLE = Table(TABLE_NAME)

    @classmethod
    def record_to_entity(cls, record):
        team = Team(
            id=record["id"],
            status=record["status"],
            name=record["name"],
            lead_id=record["lead_id"],
            division_id=record["division_id"],
        )
        return team

    @classmethod
    async def index(
        cls, limit: int = 10, offset: int = 0, name_prefix: Optional[str] = None, status: Optional[TeamStatus] = None
    ) -> List[Team]:
        query = QueryBuilder(dialect=Dialects.POSTGRESQL).from_(cls.TABLE).select("*")

        if name_prefix:
            query = query.where(Lower(cls.TABLE.name).like(name_prefix))

        if status:
            query = query.where(cls.TABLE.status == status)

        query = query[offset:limit]
        sql = query.get_sql()
        async with db_connection() as connection:
            records = await connection.fetch(sql)
            teams = [cls.record_to_entity(record) for record in records]
            return teams

    @classmethod
    async def _save(cls, connection, team: Team):
        records = await connection.fetchrow(
            f"INSERT INTO {cls.TABLE_NAME} (status, name, lead_id, division_id) VALUES ($1, $2, $3, $4) RETURNING *",
            team.status,
            team.name,
            team.lead_id,
            team.division_id,
        )
        return records

    @classmethod
    async def _update(cls, connection, team: Team):
        records = await connection.fetchrow(
            f"UPDATE {cls.TABLE_NAME} SET status=$2, name=$3, lead_id=$4, division_id=$5 WHERE id=$1 RETURNING *",
            team.id,
            team.status,
            team.name,
            team.lead_id,
        )
        return records
