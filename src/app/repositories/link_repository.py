from pypika import Table

from app.models.link_model import Link
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class LinkRepository(BaseRepository):
    ENTITY = Link

    TABLE_NAME = "links"
    TABLE = Table(TABLE_NAME)

    @classmethod
    async def upsert(cls, link: Link):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                        INSERT INTO {cls.TABLE_NAME}
                        (name, link, employee_id)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (id) DO UPDATE SET
                            name = EXCLUDED.name,
                            link = EXCLUDED.link,
                            employee_id = EXCLUDED.employee_id
                        RETURNING *
                        """,
                *cls.model_to_tuple(link),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return (
            model.name,
            model.link,
            model.employee_id,
        )

    @classmethod
    async def delete(cls, id: int) -> bool:
        async with db_connection() as connection:
            await connection.execute(f"DELETE FROM {cls.TABLE_NAME} WHERE id=$1;", id)

        return True

    @classmethod
    def record_to_entity(cls, record) -> Link:
        link = cls.ENTITY(id=record["id"], name=record["name"], link=record["link"], employee_id=record["employee_id"],)
        return link
