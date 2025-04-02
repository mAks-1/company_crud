from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Company
from app.core.schemas.schemas import CreateCompany


async def create_company(
    session: AsyncSession,
    company_create: CreateCompany,
) -> Company:
    company = Company(**company_create.model_dump())
    session.add(company)
    await session.commit()
    return company


async def get_all_companies(
    session: AsyncSession,
) -> Sequence[Company]:
    stmt = select(Company).order_by(Company.company_id)
    result = await session.execute(stmt)
    companies = result.scalars().all()
    return companies


async def get_company_by_id(
    session: AsyncSession,
    company_id_to_get: int,
) -> Company:
    result = await session.execute(
        select(Company).filter(Company.company_id == company_id_to_get)
    )
    company = result.scalars().first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


async def delete_company_by_id(
    session: AsyncSession,
    company_id_to_delete: int,
):
    result = await session.execute(
        select(Company).filter(Company.company_id == company_id_to_delete)
    )

    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    await session.delete(company)
    await session.commit()
    return {"message": "Company deleted successfully"}
