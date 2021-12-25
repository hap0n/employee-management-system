from typing import List

from pypika import Table

from app.models.project_position_model import ProjectPosition
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class ProjectPositionRepository(BaseRepository):
    ENTITY = ProjectPosition

    TABLE_NAME = "project_positions"
    TABLE = Table(TABLE_NAME)

    @classmethod
    def record_to_entity(cls, record):
        project_position = ProjectPosition(
            id=record["id"], position_id=record["position_id"], reports_to=record["reports_to"],
        )
        return project_position

    @classmethod
    async def upsert(cls, project_positions: ProjectPosition):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                        INSERT INTO {cls.TABLE_NAME}
                        (position_id, reports_to)
                        VALUES ($1, $2)
                        ON CONFLICT (id) DO UPDATE SET
                            position_id = EXCLUDED.position_id,
                            reports_to = EXCLUDED.reports_to
                        RETURNING *
                        """,
                *cls.model_to_tuple(project_positions),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return (
            model.position_id,
            model.reports_to,
        )

    @classmethod
    async def get_children_positions(cls, position_id) -> List[ProjectPosition]:
        async with db_connection() as connection:
            records = await connection.fetch(f"SELECT * FROM {cls.TABLE_NAME} WHERE reports_to = {position_id}")
        return [cls.record_to_entity(record) for record in records]
