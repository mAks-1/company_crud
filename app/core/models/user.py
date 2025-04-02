from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .company import Company


class User(Base):
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(unique=False)
    last_name: Mapped[str] = mapped_column(unique=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    # Зовнішній ключ для зв'язку з Company
    company_id: Mapped[int] = mapped_column(ForeignKey("companys.company_id"))

    # Відношення багатьох-до-одного з Company
    company: Mapped["Company"] = relationship(back_populates="users")
