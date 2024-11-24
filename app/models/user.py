from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100

from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey,
    UniqueConstraint,
    ARRAY,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, intpk


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str]
    first_name: Mapped[str100 | None]
    last_name: Mapped[str100 | None]
    user_detailed_info_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_detailed_info.id"), nullable=False
    )

    user_detailed_info: Mapped["UserDetailedInfo"] = relationship("UserDetailedInfo", back_populates="users")
    subscriptions: Mapped[list["Subscribe"]] = relationship(
        "Subscribe", foreign_keys="[Subscribe.user_id1]"
    )


# class User(Base):
#     __tablename__ = "user"

#     id: Mapped[intpk]
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     password: Mapped[str] = mapped_column(Text, nullable=False)
    
    


class UserDetailedInfo(Base):
    __tablename__ = "user_detailed_info"

    id: Mapped[intpk]
    crowns: Mapped[int] = mapped_column(Integer, nullable=False)
    max_crowns: Mapped[int] = mapped_column(Integer, nullable=False)
    tag: Mapped[str] = mapped_column(Text, nullable=False)
    clan_id: Mapped[int | None] = mapped_column(ForeignKey("clan.id"), nullable=True)

    clan: Mapped["Clan"] = relationship("Clan", back_populates="members")
    users: Mapped[list["User"]] = relationship("User", back_populates="user_detailed_info")


class Subscribe(Base):
    __tablename__ = "subscribe"

    id: Mapped[intpk]
    user_id1: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_id2: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    battle_type_id: Mapped[int] = mapped_column(ForeignKey("battle_type.id"), nullable=False)

    user1: Mapped["User"] = relationship("User", foreign_keys=[user_id1])
    user2: Mapped["User"] = relationship("User", foreign_keys=[user_id2])
    battle_type: Mapped["BattleType"] = relationship("BattleType", back_populates="subscriptions")


class BattleType(Base):
    __tablename__ = "battle_type"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(Text, nullable=False)

    subscriptions: Mapped[list["Subscribe"]] = relationship("Subscribe", back_populates="battle_type")


class BattleRecord(Base):
    __tablename__ = "battle_record"

    id: Mapped[intpk]
    subscribe_id: Mapped[int] = mapped_column(ForeignKey("subscribe.id"), nullable=False)
    user1_score: Mapped[int] = mapped_column(Integer, nullable=False)
    user2_score: Mapped[int] = mapped_column(Integer, nullable=False)
    user1_get_crowns: Mapped[int] = mapped_column(Integer, nullable=False)
    user2_get_crowns: Mapped[int] = mapped_column(Integer, nullable=False)
    user1_card_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    user2_card_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    replay: Mapped[str | None] = mapped_column(Text, nullable=True)

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
    name: Mapped[str] = mapped_column(Text, nullable=False)

    members: Mapped[list["UserDetailedInfo"]] = relationship("UserDetailedInfo", back_populates="clan")
