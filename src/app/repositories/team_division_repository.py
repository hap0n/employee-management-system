from typing import List

from app.models.team_model import Team
from app.utils.postgres import db_connection


class TeamDivisionRepository:
    DIVISIONS_TABLE_NAME = "divisions"
    EMPLOYEE_TEAM_XRFS = "division_team_xrfs"
    TEAMS_TABLE_NAME = "teams"

    @classmethod
    async def get_division_teams(cls, team_id: int) -> List[Team]:
        async with db_connection() as connection:
            records = await connection.fetchall(
                f"""
                SELECT
                    t.id as id,
                    t.status as status,
                    t.name as name,
                    t.lead_id as lead_id,
                    t.division_id as division_id
                FROM {cls.TEAMS_TABLE_NAME} t
                LEFT JOIN {cls.EMPLOYEE_TEAM_XRFS} xrfs
                    ON t.id = xrfs.team_id
                LEFT JOIN {cls.DIVISIONS_TABLE_NAME} d
                    ON d.id = xrfs.division_id
                WHERE t.id = {team_id}
                """
            )
        teams = [
            Team(
                id=record.id,
                status=record.status,
                name=record.name,
                lead_id=record.lead_id,
                division_id=record.division_id,
            )
            for record in records
        ]
        return teams
