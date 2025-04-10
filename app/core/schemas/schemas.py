from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    field_validator,
)
from typing import Optional
import re


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

    # ALSO NEED EMAIL VERIFICATION

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
    password: str
    company_id: int

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*()" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    company_id: Optional[int] = None
    password: Optional[str] = None


class DeleteUser(BaseModel):
    message: str


class ReadUser(UserBase):
    user_id: int
    company_id: int

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    first_name: str
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


# test
