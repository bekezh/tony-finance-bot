from aiogram import Router, F
from aiogram.types import Message
from storage.db import async_session
from storage.models import Users, Habits
from config import REMINDERS_DEFAULT

router = Router()

def register(dp): dp.include_router(router)

@router.message(F.text.startswith("/reminders"))
async def cmd_reminders(message: Message):
    parts = message.text.split(maxsplit=1)
    new_time = parts[1] if len(parts) > 1 else REMINDERS_DEFAULT
    # простая валидация HH:MM
    try:
        hh, mm = map(int, new_time.split(":"))
        assert 0 <= hh < 24 and 0 <= mm < 60
    except Exception:
        await message.answer("Формат: /reminders HH:MM (например, 19:00)")
        return
    async with async_session() as s:
        user = await Users.get_by_tg(s, message.from_user.id)
        if not user:
            await message.answer("Сначала /start")
            return
        habits = await Habits.list_active_by_user(s, user.id)
        for h in habits:
            h.reminder_time = new_time
        await s.commit()
    await message.answer(f"Время напоминаний обновлено на {new_time} для всех активных привычек.")
