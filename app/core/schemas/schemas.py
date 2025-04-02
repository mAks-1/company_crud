from pydantic import BaseModel
from typing import Optional, List


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


# User models
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class CreateUser(UserBase):
    company_id: int


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    company_id: Optional[int] = None


class ReadUser(UserBase):
    user_id: int
    company_id: int

    class Config:
        orm_mode = True
