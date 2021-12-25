from pypika import Table

from app.models.employee_model import Employee
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class EmployeeRepository(BaseRepository):
    ENTITY = Employee

    TABLE_NAME = "employees"
    TABLE = Table(TABLE_NAME)

    @classmethod
    async def upsert(cls, employee: Employee):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                INSERT INTO {cls.TABLE_NAME}
                (first_name, middle_name, last_name, info, date_of_birth, project_position_id, internal_position_id, hired_on, fired_on, status)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (id) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    middle_name = EXCLUDED.middle_name,
                    last_name = EXCLUDED.last_name,
                    info = EXCLUDED.info,
                    date_of_birth = EXCLUDED.date_of_birth,
                    project_position_id = EXCLUDED.project_position_id,
                    internal_position_id = EXCLUDED.internal_position_id,
                    hired_on = EXCLUDED.hired_on,
                    fired_on = EXCLUDED.fired_on,
                    status = EXCLUDED.status
                RETURNING *
                """,
                *cls.model_to_tuple(employee),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return (
            model.first_name,
            model.middle_name,
            model.last_name,
            model.info,
            model.date_of_birth,
            model.project_position_id,
            model.internal_position_id,
            model.hired_on,
            model.fired_on,
            model.status.value,
        )

    @classmethod
    def record_to_entity(cls, record) -> Employee:
        employee = cls.ENTITY(
            id=record["id"],
            first_name=record["first_name"],
            middle_name=record["middle_name"],
            last_name=record["last_name"],
            info=record["info"],
            date_of_birth=record["date_of_birth"],
            project_position_id=record["project_position_id"],
            internal_position_id=record["internal_position_id"],
            status=record["status"],
            hired_on=record["hired_on"],
            fired_on=record["fired_on"],
        )
        return employee

    @classmethod
    async def delete(cls, id: int) -> bool:
        async with db_connection() as connection:
            await connection.execute(f"DELETE FROM {cls.TABLE_NAME} WHERE id=$1;", id)

        return True
