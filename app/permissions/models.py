from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base

if TYPE_CHECKING:
    from app.users.models import Users
    from app.pastes.models import Pastes


class Permissions(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    paste_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[date] = mapped_column(Date)

    user: Mapped["Users"] = relationship(back_populates="users")
    paste: Mapped["Pastes"] = relationship(back_populates="pastes")

    def __str__(self):
        return f"Permission {self.id}"