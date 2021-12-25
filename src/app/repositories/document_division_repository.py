from typing import List

from app.utils.postgres import db_connection


class DocumentDivisionRepository:
    DOCUMENTS_TABLE_NAME = "documents"
    DOCUMENT_DIVISION_XRFS = "doc_division_xrfs"
    DIVISION_TABLE_NAME = "divisions"

    @classmethod
    async def get_division_docs(cls, division_id: int) -> List[int]:
        async with db_connection() as connection:
            records = await connection.execute(
                f"""
                SELECT d.id as id
                FROM {cls.DIVISION_TABLE_NAME} t 
                LEFT JOIN {cls.DOCUMENT_DIVISION_XRFS} xrfs
                    ON t.id = xrfs.division_id
                LEFT JOIN {cls.DOCUMENTS_TABLE_NAME} d
                    ON xrfs.document_id = d.id
                WHERE t.id = {division_id}
                """
            ).fetch()
            return [record.id for record in records]
