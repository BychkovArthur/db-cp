from sqlalchemy import String, DateTime, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.models.base import Base, intpk, str100

from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey,
    UniqueConstraint,
    ARRAY,
    Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, intpk
from typing import List, Optional



class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str]
    name: Mapped[str100]
    tag: Mapped[str] = mapped_column(Text, nullable=False)
    is_super_user: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_detailed_info_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_detailed_info.id"), nullable=False
    )

    user_detailed_info: Mapped["UserDetailedInfo"] = relationship("UserDetailedInfo", back_populates="users")
    # Подписки, где текущий пользователь инициатор
    subscriptions: Mapped[list["Subscribe"]] = relationship(
        "Subscribe", foreign_keys="[Subscribe.user_id1]", overlaps="user1"
    )

    # Подписки, где текущий пользователь является подписчиком
    subscribers: Mapped[list["Subscribe"]] = relationship(
        "Subscribe", foreign_keys="[Subscribe.user_id2]", overlaps="user2"
    )


class UserDetailedInfo(Base):
    __tablename__ = "user_detailed_info"

    id: Mapped[intpk]
    crowns: Mapped[int] = mapped_column(Integer, nullable=False)
    max_crowns: Mapped[int] = mapped_column(Integer, nullable=False)
    clan_id: Mapped[int | None] = mapped_column(ForeignKey("clan.id"), nullable=True)
    updated_ts: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)

    clan: Mapped["Clan"] = relationship("Clan", back_populates="members")
    users: Mapped[list["User"]] = relationship("User", back_populates="user_detailed_info")


class Subscribe(Base):
    __tablename__ = "subscribe"

    id: Mapped[intpk]
    user_id1: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_id2: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    battle_type_id: Mapped[int] = mapped_column(ForeignKey("battle_type.id"), nullable=False)

    # Связь с User через user_id1 (инициатор подписки)
    user1: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id1],
        back_populates="subscriptions",  # Поле в User, связанное с этой стороной
        overlaps="subscribers",  # Чтобы избежать конфликта
    )

    # Связь с User через user_id2 (тот, на кого подписались)
    user2: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id2],
        back_populates="subscribers",  # Поле в User, связанное с этой стороной
        overlaps="subscriptions",  # Чтобы избежать конфликта
    )

    # Связь с BattleType
    battle_type: Mapped["BattleType"] = relationship("BattleType", back_populates="subscriptions")

    # Связь с BattleRecord
    battle_records: Mapped[list["BattleRecord"]] = relationship(
        "BattleRecord", back_populates="subscribe", cascade="all,delete"
    )


class BattleType(Base):
    __tablename__ = "battle_type"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(Text, nullable=False)

    subscriptions: Mapped[list["Subscribe"]] = relationship("Subscribe", back_populates="battle_type")


class BattleRecord(Base):
    __tablename__ = "battle_record"

    id: Mapped[intpk]
    subscribe_id: Mapped[int] = mapped_column(ForeignKey("subscribe.id", ondelete="CASCADE"), nullable=False)
    user1_score: Mapped[int] = mapped_column(Integer, nullable=False)
    user2_score: Mapped[int] = mapped_column(Integer, nullable=False)
    user1_get_crowns: Mapped[int] = mapped_column(Integer, nullable=False)
    user2_get_crowns: Mapped[int] = mapped_column(Integer, nullable=False)
    user1_card_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    user2_card_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    replay: Mapped[str | None] = mapped_column(Text, nullable=True)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    winner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=False)

    subscribe: Mapped["Subscribe"] = relationship("Subscribe", back_populates="battle_records")


class Card(Base):
    __tablename__ = "card"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)


class Clan(Base):
    __tablename__ = "clan"

    id: Mapped[intpk]
    tag: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    members: Mapped[list["UserDetailedInfo"]] = relationship("UserDetailedInfo", back_populates="clan")
