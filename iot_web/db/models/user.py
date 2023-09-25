from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.sql.sqltypes import DateTime, String

from iot_web.db.base import Base


class User(Base):
    """Base model for users.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))
    last_name: Mapped[str] = mapped_column(String(length=200))
    email: Mapped[str] = mapped_column(
        String(length=200), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=200), nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    @validates("email", "name", "last_name")
    def validate_lowercase(self, _, value):
        """Validator to lowercase fields.
        """

        return value.lower()
