from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from app.database import Base
from app.pastes.schemas import VisibilityEnum

if TYPE_CHECKING:
    from app.users.models import Users


class Pastes(Base):
    __tablename__ = "pastes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    content_location: Mapped[str] = mapped_column(String)
    created_at: Mapped[date] = mapped_column(Date)
    expires_at: Mapped[date] = mapped_column(Date)
    visibility = Column(PgEnum(VisibilityEnum, name='visibility', create_type=False), nullable=False,
                                      default=VisibilityEnum.PUBLIC)
    last_visited: Mapped[date] = mapped_column(Date)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["Users"] = relationship(back_populates="users")

    def __str__(self):
        return f"Post title_name:{self.title}"
