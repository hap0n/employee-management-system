from typing import List, Optional

from pypika import Table
from pypika.enums import Dialects
from pypika.functions import Lower
from pypika.queries import QueryBuilder

from app.models.position_model import Position, PositionStatus
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class PositionRepository(BaseRepository):
    ENTITY = Position

    TABLE_NAME = "positions"
    TABLE = Table(TABLE_NAME)

    @classmethod
    def record_to_entity(cls, record):
        position = Position(id=record["id"], status=record["status"], name=record["name"],)
        return position

    @classmethod
    async def upsert(cls, position: Position):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                    INSERT INTO {cls.TABLE_NAME}
                    (status, name)
                    VALUES ($1, $2)
                    ON CONFLICT (id) DO UPDATE SET
                        status = EXCLUDED.status,
                        name = EXCLUDED.name
                    RETURNING *
                    """,
                *cls.model_to_tuple(position),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return (
            model.status,
            model.name,
        )

    @classmethod
    async def index(
        cls,
        limit: int = 10,
        offset: int = 0,
        name_prefix: Optional[str] = None,
        status: Optional[PositionStatus] = None,
    ) -> List[Position]:
        query = QueryBuilder(dialect=Dialects.POSTGRESQL).from_(cls.TABLE).select("*")

        if name_prefix:
            query = query.where(Lower(cls.TABLE.name).like(name_prefix))

        if status:
            query = query.where(cls.TABLE.status == status)

        query = query[offset:limit]
        sql = query.get_sql()
        async with db_connection() as connection:
            records = await connection.fetch(sql)
            positions = [cls.record_to_entity(record) for record in records]
            return positions
