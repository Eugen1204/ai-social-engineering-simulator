from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from social_engineering_simulator.application.services.exception_create_organization import DuplicateDepartmentsError
from social_engineering_simulator.domain.organizations.exceptions import (
    EmployeeAddError,
    EmployeeDeleteError,
    WrongIndustryError,
    DuplicateDepartmentNameError,
    DuplicateEmailError,
    ChangeDepartmentError,
    DepartmentDelError,
    DepartmentNotFoundError,
    InvalidNameOrganizationError
)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(WrongIndustryError)
    async def handler_wrong_industry(request: Request, exc: WrongIndustryError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )

    @app.exception_handler(DuplicateDepartmentsError)
    async def handler_duplicate_department(request: Request, exc: DuplicateDepartmentsError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)}
        )



