from .base import Base
from sqlalchemy.orm import mapped_column, Mapped


class Company(Base):
    company_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    company_address: Mapped[str] = mapped_column(unique=True, nullable=False)
    company_email: Mapped[str] = mapped_column(unique=True, nullable=False)
    company_phone: Mapped[str] = mapped_column(nullable=False)
