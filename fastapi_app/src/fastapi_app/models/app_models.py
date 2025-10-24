from sqlalchemy import BigInteger, Boolean, text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import TimestampMixin, Model, Base


class User(TimestampMixin, Model):
    """Модель пользователя."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
    )
    habits: Mapped[list["Habit"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User id-{self.id}>"


class Habit(TimestampMixin, Model):
    """Модель привычки."""

    __tablename__ = "habits"

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(default="", server_default="")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped[list["User"]] = relationship(back_populates="habits")

    def __repr__(self):
        return f"<Habit id-{self.id}>"
