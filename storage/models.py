import enum
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey, Text, Date, Enum, select
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON
from sqlalchemy.dialects.postgresql import JSONB

from storage.db import Base

# для кросс-СУБД простой JSON: Text с сериализацией можно заменить при необходимости
try:
    from sqlalchemy import JSON
except Exception:
    JSON = SQLITE_JSON

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=False)
    tz = Column(String(64), default="Asia/Almaty")
    consent = Column(Boolean, default=False)
    profile_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    habits = relationship("Habits", back_populates="user", lazy="selectin")

    @staticmethod
    async def get_by_tg(s: AsyncSession, tg_id: int):
        q = await s.execute(select(Users).where(Users.tg_id == tg_id))
        return q.scalar_one_or_none()

    @staticmethod
    async def get_or_create(s: AsyncSession, tg_id: int, tz: str, consent: bool):
        obj = await Users.get_by_tg(s, tg_id)
        if obj:
            obj.consent = consent
            if tz: obj.tz = tz
            return obj
        obj = Users(tg_id=tg_id, tz=tz, consent=consent)
        s.add(obj)
        await s.flush()
        return obj

    @staticmethod
    async def all(s: AsyncSession):
        q = await s.execute(select(Users))
        return q.scalars().all()

class Habits(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String(200))
    description = Column(Text, default="")
    target_per_day = Column(Integer, default=1)
    reminder_time = Column(String(5), default="19:00")  # HH:MM
    days_mask = Column(String(7), default="1111111")    # '1111100'
    active = Column(Boolean, default=True)

    user = relationship("Users", back_populates="habits")
    logs = relationship("HabitLogs", back_populates="habit", lazy="selectin")

    @staticmethod
    async def list_active_by_user(s: AsyncSession, user_id: int):
        q = await s.execute(select(Habits).where(Habits.user_id == user_id, Habits.active == True).order_by(Habits.id))
        return q.scalars().all()

    @staticmethod
    async def get_by_id(s: AsyncSession, hid: int):
        q = await s.execute(select(Habits).where(Habits.id == hid))
        return q.scalar_one_or_none()

    @staticmethod
    async def create(s: AsyncSession, **kwargs):
        obj = Habits(**kwargs)
        s.add(obj)
        await s.flush()
        return obj

class LogStatus(enum.Enum):
    done = "done"
    miss = "miss"
    skip = "skip"

class HabitLogs(Base):
    __tablename__ = "habit_logs"
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), index=True)
    date = Column(Date, default=date.today)
    status = Column(Enum(LogStatus), default=LogStatus.done)
    note = Column(Text, default="")

    habit = relationship("Habits", back_populates="logs")

    @staticmethod
    async def add(s: AsyncSession, habit_id: int, date, status: str, note: str):
        obj = HabitLogs(habit_id=habit_id, date=date, status=LogStatus(status), note=note)
        s.add(obj); await s.flush(); return obj

    @staticmethod
    async def list_by_user(s: AsyncSession, user_id: int):
        # join habits
        q = await s.execute(select(HabitLogs).join(Habits, HabitLogs.habit_id==Habits.id).where(Habits.user_id==user_id).order_by(HabitLogs.date.desc()))
        return q.scalars().all()

class Plans(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    plan_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    async def create(s: AsyncSession, **kwargs):
        obj = Plans(**kwargs); s.add(obj); await s.flush(); return obj

    @staticmethod
    async def last_by_user(s: AsyncSession, user_id: int):
        q = await s.execute(select(Plans).where(Plans.user_id==user_id).order_by(Plans.id.desc()).limit(1))
        return q.scalar_one_or_none()

class Sources(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    title = Column(String(300))
    url = Column(Text, default="")
    summary = Column(Text, default="")
    added_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    async def create(s: AsyncSession, **kwargs):
        obj = Sources(**kwargs); s.add(obj); await s.flush(); return obj

    @staticmethod
    async def list_by_user(s: AsyncSession, user_id: int, limit: int = 10):
        q = await s.execute(select(Sources).where(Sources.user_id==user_id).order_by(Sources.id.desc()).limit(limit))
        return q.scalars().all()

class AISessions(Base):
    __tablename__ = "ai_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    stage = Column(String(50))  # onboarding/dialog/format
    context_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    model = Column(String(64), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
