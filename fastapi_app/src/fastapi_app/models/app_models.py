from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import TimestampMixin, Model


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

    session: Mapped["AuthSession"] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User id-{self.id}>"


class AuthSession(TimestampMixin, Model):
    """Модель сессии аутентификации."""

    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String, unique=True, default=uuid4().hex)
    jwt: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    user: Mapped["User"] = relationship(back_populates="session")

    def __repr__(self):
        return f"<Login session: {self.session_id}>"
