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
    async def upsert(cls, division: Division):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                    INSERT INTO {cls.TABLE_NAME}
                    (status, name, lead_id)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (id) DO UPDATE SET
                        status = EXCLUDED.status,
                        name = EXCLUDED.name,
                        lead_id = EXCLUDED.lead_id
                    RETURNING *
                    """,
                *cls.model_to_tuple(division),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return (model.status, model.name, model.lead_id)

    @classmethod
    def record_to_entity(cls, record) -> Division:
        division = cls.ENTITY(id=record["id"], status=record["status"], name=record["name"], lead_id=record["lead_id"],)
        return division
