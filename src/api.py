import os

import uvicorn
from fastapi import APIRouter, FastAPI

from app.routes.company_info_routes import company_info_router
from app.routes.division_routes import division_router
from app.routes.holiday_routes import holiday_router
from app.routes.position_routes import position_router
from app.routes.team_routes import team_router
from app.utils.fastapi_metadata import tags_metadata


def create_app():
    app = FastAPI(
        openapi_url="/api/openapi.json", docs_url="/api/docs/", redoc_url="/api/redoc/", openapi_tags=tags_metadata
    )

    nestable_router = APIRouter()
    app.include_router(prefix="/api", router=nestable_router)
    app.include_router(prefix="/positions", router=position_router)
    app.include_router(prefix="/divisions", router=division_router)
    app.include_router(prefix="/teams", router=team_router)
    app.include_router(prefix="/holidays", router=holiday_router)
    app.include_router(prefix="/company_info", router=company_info_router)

    return app


def main():
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("EMS_API_PORT")), loop="asyncio")


if __name__ == "__main__":
    main()
