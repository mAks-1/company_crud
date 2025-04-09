from pydantic import BaseModel, EmailStr, ConfigDict
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


# User models
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str

    @field_validator("username")
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 20:
            raise ValueError("Username must be less than 20 characters")
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, underscores, and hyphens"
            )
        return v


class CreateUser(UserBase):
    company_id: int


class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    company_id: Optional[int] = None


class DeleteUser(BaseModel):
    message: str


class ReadUser(UserBase):
    user_id: int
    company_id: int

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
