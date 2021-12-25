from pypika import Table

from app.models.phone_model import Phone
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class PhoneRepository(BaseRepository):
    ENTITY = Phone

    TABLE_NAME = "phone_numbers"
    TABLE = Table(TABLE_NAME)

    @classmethod
    async def upsert(cls, phone: Phone):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                    INSERT INTO {cls.TABLE_NAME}
                    (phone, status, employee_id)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (id) DO UPDATE SET
                        phone = EXCLUDED.phone,
                        status = EXCLUDED.status,
                        employee_id = EXCLUDED.employee_id
                    RETURNING *
                    """,
                *cls.model_to_tuple(phone),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return (
            model.phone,
            model.status,
            model.employee_id,
        )

    @classmethod
    async def delete(cls, id: int) -> bool:
        async with db_connection() as connection:
            await connection.execute(f"DELETE FROM {cls.TABLE_NAME} WHERE id=$1;", id)

        return True

    @classmethod
    def record_to_entity(cls, record) -> Phone:
        phone = cls.ENTITY(
            id=record["id"], phone=record["phone"], status=record["status"], employee_id=record["employee_id"],
        )
        return phone
