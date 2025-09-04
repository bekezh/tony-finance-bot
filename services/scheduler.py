from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zoneinfo import ZoneInfo
from datetime import datetime
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from storage.db import async_session
from storage.models import Users, Habits

from utils.tz import DEFAULT_TZ

async def send_reminder(bot: Bot, tg_id: int, habit_title: str, habit_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Выполнено", callback_data=f"habit_action:done:{habit_id}"),
        InlineKeyboardButton(text="⏭ Пропуск", callback_data=f"habit_action:skip:{habit_id}")
    ]])
    await bot.send_message(tg_id, f"Напоминание: {habit_title}", reply_markup=kb)

async def check_and_send(bot: Bot):
    async with async_session() as s:
        users = await Users.all(s)
        for u in users:
            tz = ZoneInfo(u.tz or DEFAULT_TZ)
            now = datetime.now(tz)
            hm = now.strftime("%H:%M")
            dow = now.weekday()  # 0=Mon
            habits = await Habits.list_active_by_user(s, u.id)
            for h in habits:
                mask = h.days_mask or "1111111"
                if len(mask) == 7 and mask[dow] == "1" and h.reminder_time == hm:
                    await send_reminder(bot, u.tg_id, h.title, h.id)

async def init_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone=ZoneInfo(DEFAULT_TZ))
    # каждый 60 сек.
    scheduler.add_job(check_and_send, "interval", seconds=60, args=[bot])
    scheduler.start()
