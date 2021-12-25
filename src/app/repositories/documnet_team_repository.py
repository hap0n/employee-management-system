from typing import List

from app.utils.postgres import db_connection


class DocumentTeamRepository:
    DOCUMENTS_TABLE_NAME = "documents"
    DOCUMENT_TEAM_XRFS = "doc_team_xrfs"
    TEAM_TABLE_NAME = "teams"

    @classmethod
    async def get_team_docs(cls, team_id: int) -> List[int]:
        async with db_connection() as connection:
            records = await connection.fetch(
                f"""
                SELECT d.id as id
                FROM {cls.TEAM_TABLE_NAME} t 
                LEFT JOIN {cls.DOCUMENT_TEAM_XRFS} xrfs
                    ON t.id = xrfs.team_id
                LEFT JOIN {cls.DOCUMENTS_TABLE_NAME} d
                    ON xrfs.document_id = d.id
                WHERE t.id = {team_id}
                """
            )
            return [record.id for record in records]
