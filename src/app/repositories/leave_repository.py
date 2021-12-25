from pypika import Table

from app.models.leave_model import Leave
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class LeaveRepository(BaseRepository):
    ENTITY = Leave

    TABLE_NAME = "leaves"
    TABLE = Table(TABLE_NAME)

    @classmethod
    async def upsert(cls, leave: Leave):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                INSERT INTO {cls.TABLE_NAME}
                (leave_type, start_date, end_date, status, approved_by, requested_at, approved_at, employee_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (id) DO UPDATE SET
                    leave_type = EXCLUDED.leave_type,
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date,
                    status = EXCLUDED.status,
                    approved_by = EXCLUDED.approved_by,
                    requested_at = EXCLUDED.requested_at,
                    approved_at = EXCLUDED.approved_at,
                    employee_id = EXCLUDED.employee_id
                RETURNING *
                """,
                *cls.model_to_tuple(leave),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return (
            model.leave_type,
            model.start_date,
            model.end_date,
            model.leave_status,
            model.approved_by,
            model.requested_at,
            model.approved_at,
            model.employee_id,
        )

    @classmethod
    async def delete(cls, id: int) -> bool:
        async with db_connection() as connection:
            await connection.execute(f"DELETE FROM {cls.TABLE_NAME} WHERE id=$1;", id)

        return True

    @classmethod
    def record_to_entity(cls, record) -> Leave:
        leave = cls.ENTITY(
            id=record["id"],
            leave_type=record["leave_type"],
            start_date=record["start_date"],
            end_date=record["end_date"],
            leave_status=record["status"],
            approved_by=record["approved_by"],
            requested_at=record["requested_at"],
            approved_at=record["approved_at"],
            employee_id=record["employee_id"],
        )
        return leave
