from fastapi import APIRouter

from app.models.company_info_model import CompanyInfo
from app.repositories.company_info_repository import CompanyInfoRepository
from app.repositories.holiday_repository import HolidayRepository
from app.responces.company_info_response import CompanyInfoResponse

company_info_router = APIRouter()


@company_info_router.get("/info", response_model=CompanyInfoResponse, tags=["CompanyInfo"])
async def get_company_info() -> CompanyInfoResponse:
    company_info = await CompanyInfoRepository.get_company_info()
    document_ids = await CompanyInfoRepository.get_company_docs()
    holidays = await HolidayRepository.get_list()

    response = CompanyInfoResponse(
        name=company_info.name, description=company_info.description, holidays=holidays, document_ids=document_ids
    )
    return response


@company_info_router.put("/update", response_model=CompanyInfo, tags=["CompanyInfo"])
async def update_position(company_info: CompanyInfo):
    company_info = await CompanyInfoRepository.update(company_info)
    return company_info
