from pypika import Table

from app.models.document_model import Document
from app.repositories.base_repository import BaseRepository
from app.utils.postgres import db_connection


class DocumentRepository(BaseRepository):
    ENTITY = Document

    TABLE_NAME = "documents"
    TABLE = Table(TABLE_NAME)

    @classmethod
    async def upsert(cls, document: Document):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                        INSERT INTO {cls.TABLE_NAME} (s3_bucket)
                        VALUES ($1)
                        ON CONFLICT (id) DO UPDATE SET
                            s3_bucket = EXCLUDED.s3_bucket
                        RETURNING *
                        """,
                cls.model_to_tuple(document),
            )

        return cls.record_to_entity(record)

    @classmethod
    def model_to_tuple(cls, model):
        return model.s3_bucket

    @classmethod
    async def delete(cls, id: int) -> bool:
        async with db_connection() as connection:
            await connection.execute(f"DELETE FROM {cls.TABLE_NAME} WHERE id=$1;", id)

        return True

    @classmethod
    def record_to_entity(cls, record) -> Document:
        document = cls.ENTITY(id=record["id"], s3_bucket=record["s3_bucket"],)
        return document
