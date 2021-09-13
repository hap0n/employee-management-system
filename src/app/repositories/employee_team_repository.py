from typing import List

from app.utils.postgres import db_connection


class EmployeeTeamRepository:
    EMPLOYEES_TABLE_NAME = "employees"
    EMPLOYEE_TEAM_XRFS = "employee_team_xrfs"
    TEAMS_TABLE_NAME = "teams"

    @classmethod
    async def get_team_employees(cls, team_id: int) -> List[int]:
        async with db_connection() as connection:
            records = await connection.fetchall(
                f"""
                SELECT t.id as id
                FROM {cls.TEAMS_TABLE_NAME} t
                LEFT JOIN {cls.EMPLOYEE_TEAM_XRFS} xrfs
                    ON t.id = xrfs.team_id
                LEFT JOIN {cls.EMPLOYEES_TABLE_NAME} e
                    ON e.id = xrfs.employee_id
                WHERE t.id = {team_id}
                """
            )
        return [record.id for record in records]
