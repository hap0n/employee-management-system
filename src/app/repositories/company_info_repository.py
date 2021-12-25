from typing import List

from app.errors.service_error import ServiceError
from app.models.company_info_model import CompanyInfo
from app.utils.postgres import db_connection


class CompanyInfoRepository:
    COMPANY_INF_TABLE_NAME = "company_info"
    COMPANY_DOCUMENTS_TABLE_NAME = "company_docs"

    @classmethod
    def record_to_entity(cls, record):
        company_info = CompanyInfo(name=record["name"], description=record["description"], lead_id=record["lead_id"],)
        return company_info

    @classmethod
    def model_to_tuple(cls, model):
        return (model.name, model.description, model.lead_id)

    @classmethod
    async def get_company_info(cls):
        async with db_connection() as connection:
            record = await connection.fetchrow(f"SELECT * FROM {cls.COMPANY_INF_TABLE_NAME}")
            if record is None:
                raise ServiceError(message="company_info table is empty")

            return cls.record_to_entity(record)

    @classmethod
    async def upsert(cls, company_info: CompanyInfo):
        async with db_connection() as connection:
            record = await connection.fetchrow(
                f"""
                    INSERT INTO {cls.COMPANY_INF_TABLE_NAME}
                    (name, description, lead_id)
                    VALUES ($1, $2, $3)
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        description = EXCLUDED.description,
                        lead_id = EXCLUDED.lead_id
                    RETURNING *
                    """,
                *cls.model_to_tuple(company_info),
            )

        return cls.record_to_entity(record)

    @classmethod
    async def get_company_docs(cls) -> List[int]:
        async with db_connection() as connection:
            records = await connection.fetch(f"SELECT * FROM {cls.COMPANY_DOCUMENTS_TABLE_NAME}")

        return records
