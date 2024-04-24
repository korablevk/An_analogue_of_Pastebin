from datetime import date
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at: Mapped[date] = mapped_column(Date)
    last_login: Mapped[date] = mapped_column(Date)

    def __str__(self):
        return f"Пользователь {self.email}"
