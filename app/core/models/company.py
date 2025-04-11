from typing import List, TYPE_CHECKING

from .base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from .user import User


class Company(Base):
    company_id: Mapped[int] = mapped_column(primary_key=True)

    company_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    company_address: Mapped[str] = mapped_column(unique=False, nullable=False)
    company_email: Mapped[str] = mapped_column(unique=True, nullable=False)
    company_phone: Mapped[str] = mapped_column(nullable=False)
    company_description: Mapped[str] = mapped_column(nullable=True)

    # Відношення один-до-багатьох з User
    users: Mapped[List["User"]] = relationship(back_populates="company")
