from typing import List, Union

from app.models.internal_position_model import InternalPosition
from app.models.position_model import PositionType
from app.models.project_position_model import ProjectPosition
from app.repositories.internal_position_repository import InternalPositionRepository
from app.repositories.project_position_repository import ProjectPositionRepository


class PositionsService:
    @classmethod
    async def get_path_to_root(
        cls, position_id: int, position_type: PositionType
    ) -> List[Union[InternalPosition, ProjectPosition]]:
        if position_type is PositionType.INTERNAL:
            position_repository = InternalPositionRepository
        else:
            position_repository = ProjectPositionRepository

        path = []
        while True:
            root_position = position_repository.get_by_id(position_id)
            if root_position:
                path.append(root_position)
                position_id = root_position.id
            else:
                break

        return path
