from pydantic import BaseModel


class CompanyBase(BaseModel):
    company_name: str
    company_address: str
    company_email: str
    company_phone: str


class CreateCompany(CompanyBase):
    pass


class UpdateCompany(CompanyBase):
    pass


class DeleteCompany(CompanyBase):
    message: str


class ReadCompany(CompanyBase):
    company_id: int

    class Config:
        orm_mode = True
