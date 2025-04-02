from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Company, db_helper
from app.core.schemas.schemas import ReadCompany, CreateCompany
from app.crud import companies as crud_companies

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.get("", response_model=list[ReadCompany])
async def get_companies(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    companies = await crud_companies.get_all_companies(session=session)
    return companies if companies else []


@router.post("", response_model=CreateCompany)
async def create_company(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    company_create: CreateCompany,
):
    return await crud_companies.create_company(
        session=session, company_create=company_create
    )

