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
            id=record["id"],
            position_id=record["position_id"],
            reports_to=record["reports_to"],
        )
        return project_position

    @classmethod
    async def _save(cls, connection, project_position: ProjectPosition):
        records = await connection.fetchrow(
            f"INSERT INTO {cls.TABLE_NAME} (position_id, reports_to) VALUES ($1, $2) RETURNING *",
            project_position.position_id,
            project_position.reports_to,
        )
        return records

    @classmethod
    async def _update(cls, connection, project_position: ProjectPosition):
        records = await connection.fetchrow(
            f"UPDATE {cls.TABLE_NAME} SET position_id=$2, reports_to=$3 WHERE id=$1 RETURNING *",
            project_position.id,
            project_position.position_id,
            project_position.reports_to,
        )
        return records

    @classmethod
    async def get_children_positions(cls, position_id) -> List[ProjectPosition]:
        async with db_connection() as connection:
            records = await connection.fetchall(f"SELECT * FROM {cls.TABLE_NAME} WHERE reports_to = {position_id}")
        return [cls.record_to_entity(record) for record in records]
