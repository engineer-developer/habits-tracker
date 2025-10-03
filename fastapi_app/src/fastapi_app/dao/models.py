"""Модуль создания моделей базы данных."""

import datetime
from pathlib import Path
from typing import List, Optional

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Table,
    UniqueConstraint,
    select,
    text,
    BigInteger,
    Boolean,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dao.base_model import Model, TimestampMixin


class User(TimestampMixin, Model):
    """Класс пользователей."""

    __tablename__ = "users"

    name: Mapped[str]
    password: Mapped[str]
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


# class ApiKey(Model):  # type: ignore[name-defined]
#     # Api keys database table
#     __tablename__ = "api_keys"
#     __table_args__ = (UniqueConstraint("api_key", "user_id"),)
#
#     api_key: Mapped[str] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id"),
#         primary_key=True,
#     )
#
#
# followers = Table(
#     "followers",
#     Model.metadata,
#     Column("follower_id", ForeignKey("users.id"), primary_key=True),
#     Column("followed_id", ForeignKey("users.id"), primary_key=True),
# )
#
#
# class User(Model):  # type: ignore[name-defined]
#     # Users database table
#     __tablename__ = "users"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(200), nullable=False)
#
#     following: Mapped[list["User"]] = relationship(
#         secondary=followers,
#         primaryjoin=(followers.c.follower_id == id),
#         secondaryjoin=(followers.c.followed_id == id),
#         back_populates="followers",
#         lazy="immediate",
#     )
#     followers: Mapped[list["User"]] = relationship(
#         secondary=followers,
#         primaryjoin=(followers.c.followed_id == id),
#         secondaryjoin=(followers.c.follower_id == id),
#         back_populates="following",
#         lazy="immediate",
#     )
#     tweets: Mapped[list["Tweet"]] = relationship(
#         back_populates="author",
#         cascade="all, delete-orphan",
#         lazy="selectin",
#     )
#     likes: Mapped[list["Like"]] = relationship(
#         back_populates="user",
#         cascade="all, delete-orphan",
#         lazy="selectin",
#     )
#
#     async def follow(self, user, session):
#         # Subscribe for user
#         is_following = await self.is_following(user, session)
#         if not is_following:
#             self.following.append(user)
#             await session.commit()
#             return self
#
#     async def unfollow(self, user, session):
#         # Unsubscribe from user
#         is_following = await self.is_following(user, session)
#         if is_following:
#             self.following.remove(user)
#             await session.commit()
#             return self
#
#     async def is_following(self, user, session) -> bool:
#         # Check user is following
#         stmt = select(User).where(
#             User.id == self.id,
#             User.following.contains(user),
#         )
#         result = await session.execute(stmt)
#         if result.one_or_none():
#             return True
#         return False
#
#     def __repr__(self) -> str:
#         return f"<{type(self).__name__}> {self.name}"
#
#
# class Tweet(Model):  # type: ignore[name-defined]
#     # Tweets database table
#     __tablename__ = "tweets"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id", ondelete="CASCADE"),
#     )
#     content: Mapped[str] = mapped_column(nullable=False)
#
#     author: Mapped["User"] = relationship(  # type: ignore  # noqa: F821
#         back_populates="tweets",
#         lazy="selectin",
#     )
#     likes: Mapped[List["Like"]] = relationship(
#         back_populates="tweet",
#         cascade="all, delete-orphan",
#         lazy="selectin",
#     )
#     medias: Mapped[List["Media"]] = relationship(
#         back_populates="tweet",
#         cascade="all, delete-orphan",
#         lazy="selectin",
#     )
#     create_at: Mapped[datetime.datetime] = mapped_column(
#         server_default=text("TIMEZONE('utc', now())"),
#     )
#     attachments: Mapped[list[str]] = mapped_column(
#         ARRAY(String),
#     )
#
#     def delete_attachments(self, media_folder) -> None:
#         """Delete attachment files from host"""
#         if len(self.attachments) > 0:
#             for file in list(self.attachments):
#                 file_path = Path(media_folder) / file
#                 if file_path.exists():
#                     file_path.unlink()
#
#
# class Media(Model):  # type: ignore[name-defined]
#     # Medias database table
#     __tablename__ = "media"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(nullable=False)
#     tweet_id: Mapped[Optional[int]] = mapped_column(
#         ForeignKey("tweets.id", ondelete="CASCADE"),
#     )
#
#     tweet: Mapped["Tweet"] = relationship(  # type: ignore  # noqa: F821
#         back_populates="medias",
#         lazy="selectin",
#     )
#
#
# class Like(Model):  # type: ignore[name-defined]
#     # Likes database table
#     __tablename__ = "likes"
#     __table_args__ = (UniqueConstraint("tweet_id", "user_id"),)
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     tweet_id: Mapped[int] = mapped_column(
#         ForeignKey(
#             "tweets.id",
#             ondelete="CASCADE",
#         )
#     )
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#
#     tweet: Mapped["Tweet"] = relationship(  # type: ignore  # noqa:  F821
#         back_populates="likes",
#         lazy="selectin",
#     )
#     user: Mapped["User"] = relationship(  # type: ignore  # noqa:  F821
#         back_populates="likes",
#         lazy="selectin",
#     )
