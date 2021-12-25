from abc import abstractmethod
from typing import List, Optional

from pydantic import BaseModel
from pypika import Query
from pypika.functions import Lower

from app.errors.entity_not_found_errors import EntityNotFound
from app.utils.postgres import db_connection


class BaseRepository:
    ENTITY = BaseModel
    TABLE_NAME: str

    @classmethod
    async def get_list(cls, limit: int = 10, offset: int = 0):
        async with db_connection() as connection:
            records = await connection.fetch(f"SELECT * FROM {cls.TABLE_NAME} LIMIT {limit} OFFSET {offset}")
            return [cls.record_to_entity(record) for record in records]

    @classmethod
    @abstractmethod
    def record_to_entity(cls, record):
        pass

    @classmethod
    @abstractmethod
    def model_to_tuple(cls, model):
        pass

    @classmethod
    @abstractmethod
    async def upsert(cls, entity):
        pass

    @classmethod
    async def get_by_id(cls, id: int) -> Optional[BaseModel]:
        async with db_connection() as connection:
            record = await connection.fetchrow(f"SELECT * FROM {cls.TABLE_NAME} WHERE id={id};")

            if record is None:
                raise EntityNotFound(message=f"{cls.ENTITY} with id {id} not found!")

            return cls.record_to_entity(record)

    @classmethod
    async def find_by_name(cls, limit: int, offset: int, query: str) -> List[BaseModel]:
        async with db_connection() as connection:
            sql_query = Query.from_(cls.TABLE).select("*")

            if query:
                sql_query = sql_query.where(Lower(cls.TABLE.name).like(f"%{query}%"))

            records = await connection.fetch(sql_query[offset:limit].get_sql())

        return [cls.record_to_entity(record) for record in records]
