from typing import List

from app.errors.service_error import ServiceError
from app.models.company_info_model import CompanyInfo
from app.utils.postgres import db_connection


class CompanyInfoRepository:
    COMPANY_INF_TABLE_NAME = "company_info"
    COMPANY_DOCUMENTS_TABLE_NAME = "company_docs"
    
    @classmethod
    def record_to_entity(cls, record):
        company_info = CompanyInfo(
            name=record["name"],
            description=record["description"],
            lead_id=record["lead_id"],
        )
        return company_info
    
    @classmethod
    async def get_company_info(cls):
        async with db_connection() as connection:
            record = await connection.fetchone(f"SELECT * FROM {cls.COMPANY_INF_TABLE_NAME}")
            if record is None:
                raise ServiceError(message="company_info table is empty")

            return cls.record_to_entity(record)

    @classmethod
    async def update(cls, company_info: CompanyInfo) -> CompanyInfo:
        async with db_connection() as connection:
            try:
                record = await connection.fetchone(
                    f"UPDATE {cls.COMPANY_INF_TABLE_NAME} SET name=$1, lead_id=$2, description=$3 RETURNING *",
                    company_info.name,
                    company_info.lead_id,
                    company_info.description,
                )
            except Exception:
                raise ServiceError(message="company_info table is empty")

        return cls.record_to_entity(record)

    @classmethod
    async def get_company_docs(cls) -> List[int]:
        async with db_connection() as connection:
            records = await connection.fetchall(f"SELECT * FROM {cls.COMPANY_DOCUMENTS_TABLE_NAME}")

        return records
