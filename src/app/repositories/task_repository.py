from pypika import Table

from app.models.task_model import Task
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class TaskRepository(BaseRepository):
    ENTITY = Task

    TABLE_NAME = "tasks"
    TABLE = Table(TABLE_NAME)

    @classmethod
    async def upsert(cls, task: Task):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                    INSERT INTO {cls.TABLE_NAME}
                    (title, description, priority, status, assignee_id, reporter_id, created_at, employee_id)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        description = EXCLUDED.description,
                        priority = EXCLUDED.priority,
                        status = EXCLUDED.status,
                        assignee_id = EXCLUDED.assignee_id,
                        reporter_id = EXCLUDED.reporter_id,
                        created_at = EXCLUDED.created_at,
                        employee_id = EXCLUDED.employee_id
                    RETURNING *
                    """,
                *cls.model_to_tuple(task),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return (
            model.title,
            model.description,
            model.task_priority,
            model.task_status,
            model.assignee_id,
            model.reporter_id,
            model.created_at,
            model.employee_id,
        )

    @classmethod
    async def delete(cls, id: int) -> bool:
        async with db_connection() as connection:
            await connection.execute(f"DELETE FROM {cls.TABLE_NAME} WHERE id=$1;", id)

        return True

    @classmethod
    def record_to_entity(cls, record) -> Task:
        task = cls.ENTITY(
            id=record["id"],
            title=record["title"],
            description=record["description"],
            task_priority=record["priority"],
            task_status=record["status"],
            assignee_id=record["assignee_id"],
            reporter_id=record["reporter_id"],
            created_at=record["created_at"],
            employee_id=record["employee_id"],
        )
        return task
