from pydantic import BaseModel
from typing import Optional


class CompanyBase(BaseModel):
    company_name: str
    company_address: str
    company_email: str
    company_phone: str


class CreateCompany(CompanyBase):
    pass


class UpdateCompany(BaseModel):
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    company_email: Optional[str] = None
    company_phone: Optional[str] = None


class DeleteCompany(BaseModel):
    message: str


class ReadCompany(CompanyBase):
    company_id: int

    class Config:
        orm_mode = True
