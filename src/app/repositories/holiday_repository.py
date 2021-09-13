from datetime import date
from typing import List

from pypika import Table

from app.models.holiday_model import Holiday
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class HolidayRepository(BaseRepository):
    ENTITY = Holiday

    TABLE_NAME = "holidays"
    TABLE = Table(TABLE_NAME)

    @classmethod
    async def _save(cls, connection, holiday: Holiday):
        records = await connection.execute(
            f"INSERT INTO {cls.TABLE_NAME} (name, date) VALUES ($1, $2) RETURNING *", holiday.name, holiday.date,
        ).fetchrow()
        return records

    @classmethod
    async def _update(cls, connection, holiday: Holiday):
        records = await connection.execute(
            f"UPDATE {cls.TABLE_NAME} SET name=$2, date=$3 WHERE id=$1 RETURNING *",
            holiday.id,
            holiday.name,
            holiday.date,
        ).fetchrow()
        return records

    @classmethod
    async def delete(cls, id: int) -> bool:
        async with db_connection() as connection:
            await connection.execute(f"DELETE FROM {cls.TABLE_NAME} WHERE id=$1;", id)

        return True

    @classmethod
    async def between(cls, start_date: date, end_date: date) -> List[Holiday]:
        async with db_connection() as connection:
            records = await connection.execute(
                f"SELECT * FROM {cls.TABLE_NAME} WHERE date > $1 AND date < $2", start_date, end_date
            ).fetchall()
        return [cls.record_to_entity(record) for record in records]

    @classmethod
    def record_to_entity(cls, record) -> Holiday:
        holiday = cls.ENTITY(
            id=record["id"], date=record["date"], name=record["name"]
        )
        return holiday
