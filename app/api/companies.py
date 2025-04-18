from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.core.schemas.schemas import (
    ReadCompany,
    CreateCompany,
    DeleteCompany,
    UpdateCompany,
)
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


@router.get("/{company_id}", response_model=ReadCompany)
async def get_company_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    company_id: int,
):
    company = await crud_companies.get_company_by_id(
        session=session, company_id_to_get=company_id
    )
    return company


@router.delete("/{company_id}", response_model=DeleteCompany)
async def delete_company(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    company_id: int,
):
    company = await crud_companies.delete_company_by_id(
        session=session,
        company_id_to_delete=company_id,
    )

    return company


@router.patch("/{company_id}", response_model=ReadCompany)
async def update_company_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    company_update: UpdateCompany,
    company_id: int,
):
    result = await crud_companies.update_company_by_id(
        session=session,
        company_update=company_update,
        company_id_to_update=company_id,
    )

    return result
