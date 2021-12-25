from typing import List, Optional

from fastapi import APIRouter

from app.models.employee_model import Employee
from app.repositories.employee_repository import EmployeeRepository

employee_router = APIRouter()


@employee_router.get("/", response_model=List[Employee], tags=["Employee"])
async def get_list() -> List[Employee]:
    employees = await EmployeeRepository.get_list()
    return employees


@employee_router.get("/{employee_id}", response_model=Employee, tags=["Employee"])
async def get_employee(employee_id: int) -> Optional[Employee]:
    employee = await EmployeeRepository.get_by_id(employee_id)
    return employee


@employee_router.post("/update", response_model=Employee, tags=["Employee"])
async def update_employee(employee: Employee):
    employee = await EmployeeRepository.upsert(employee)
    return employee


@employee_router.put("/create", response_model=Employee, tags=["Employee"])
async def create_employee(employee: Employee):
    employee = await EmployeeRepository.upsert(employee)
    return employee
