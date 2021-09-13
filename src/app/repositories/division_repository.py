from typing import List, Optional

from pypika import Table
from pypika.enums import Dialects
from pypika.functions import Lower
from pypika.queries import QueryBuilder

from app.models.division_model import Division, DivisionStatus
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class DivisionRepository(BaseRepository):
    ENTITY = Division

    TABLE_NAME = "divisions"
    TABLE = Table(TABLE_NAME)

    @classmethod
    async def index(
        cls,
        limit: int = 10,
        offset: int = 0,
        name_prefix: Optional[str] = None,
        status: Optional[DivisionStatus] = None,
    ) -> List[Division]:
        query = QueryBuilder(dialect=Dialects.POSTGRESQL).from_(cls.TABLE).select("*")

        if name_prefix:
            query = query.where(Lower(cls.TABLE.name).like(name_prefix))

        if status:
            query = query.where(cls.TABLE.status == status)

        query = query[offset:limit]
        sql = query.get_sql()
        async with db_connection() as connection:
            records = await connection.fetch(sql)
            divisions = [
                Division(id=record["id"], status=record["status"], name=record["name"], lead_id=record["lead_id"],)
                for record in records
            ]
            return divisions

    @classmethod
    async def _save(cls, connection, division: Division):
        records = await connection.fetchrow(
            f"INSERT INTO {cls.TABLE_NAME} (status, name, lead_id) VALUES ($1, $2, $3) RETURNING *",
            division.status,
            division.name,
            division.lead_id,
        )
        return records

    @classmethod
    async def _update(cls, connection, division: Division):
        records = await connection.fetchrow(
            f"UPDATE {cls.TABLE_NAME} SET status=$2, name=$3, lead_id=$4 WHERE id=$1 RETURNING *",
            division.id,
            division.status,
            division.name,
            division.lead_id,
        )
        return records
