from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date
from storage.db import async_session
from storage.models import Habits, HabitLogs, Users

router = Router()

def register(dp): dp.include_router(router)

def habit_inline(h):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Выполнено", callback_data=f"habit_action:done:{h.id}"),
        InlineKeyboardButton(text="⏭ Пропуск", callback_data=f"habit_action:skip:{h.id}")
    ]])

@router.message(F.text == "/habits")
async def cmd_habits(message: Message):
    async with async_session() as s:
        user = await Users.get_by_tg(s, message.from_user.id)
        if not user:
            await message.answer("Сначала /start")
            return
        habits = await Habits.list_active_by_user(s, user.id)
        if not habits:
            await message.answer("У вас нет активных привычек. Сгенерируйте план: /plan")
            return
        for h in habits:
            await message.answer(f"• <b>{h.title}</b> — напоминание {h.reminder_time}", reply_markup=habit_inline(h))

@router.callback_query(F.data.startswith("habit_action:"))
async def cb_habit_action(cb: CallbackQuery):
    parts = cb.data.split(":")
    action, habit_id = parts[1], int(parts[2])
    async with async_session() as s:
        h = await Habits.get_by_id(s, habit_id)
        if not h:
            await cb.answer("Не найдено", show_alert=True)
            return
        status = "done" if action == "done" else "skip"
        await HabitLogs.add(s, habit_id=h.id, date=date.today(), status=status, note="")
        await s.commit()
    await cb.message.edit_text(f"<b>{h.title}</b> — отмечено: {('выполнено' if status=='done' else 'пропуск')}")
    await cb.answer("Отмечено")
