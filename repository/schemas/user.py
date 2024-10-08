from repository.schemas import Base, SessionType
from repository.schemas.item import Item

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, Enum as DBEnum

from typing import Optional, List

from uuid import UUID, uuid4

from datetime import datetime, timezone, date


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=datetime.now(timezone.utc)
    )
    fullname: Mapped[str] = mapped_column()
    dob: Mapped[date] = mapped_column()
    address: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()
    backup_email: Mapped[Optional[str]] = mapped_column()
    key: Mapped["CryptoKey"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[List["SessionInfo"]] = relationship(
        cascade="all, delete-orphan", back_populates="user"
    )
    items: Mapped[List["Item"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class CryptoKey(Base):
    __tablename__ = "crypto_keys"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    enc_pri: Mapped[str] = mapped_column()
    public_key: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="key", single_parent=True)

    __table_args__ = (UniqueConstraint("user_id"),)


class SessionInfo(Base):
    __tablename__ = "session_infos"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    location: Mapped[str] = mapped_column()
    ip: Mapped[str] = mapped_column()
    user_agent: Mapped[str] = mapped_column()
    device_fk: Mapped[str] = mapped_column(ForeignKey("devices.id"))
    device: Mapped["Device"] = relationship()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="sessions")
    type: Mapped["SessionType"] = mapped_column(DBEnum(SessionType))
    token: Mapped[str] = mapped_column()


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[Optional[datetime]] = mapped_column()
    member_counts: Mapped[int] = mapped_column()
    members: Mapped[List["UserInGroup"]] = relationship()


class UserInGroup(Base):
    __tablename__ = "users_in_groups"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    role: Mapped[str] = mapped_column()
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    user: Mapped["User"] = relationship()


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    device_id: Mapped[UUID] = mapped_column(unique=True)
    browser: Mapped[str] = mapped_column()
    os: Mapped[str] = mapped_column()
    device_type: Mapped[str] = mapped_column()
