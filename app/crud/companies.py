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


