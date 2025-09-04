from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_tracking(habit_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Выполнено", callback_data=f"habit_action:done:{habit_id}"),
        InlineKeyboardButton(text="⏭ Пропуск", callback_data=f"habit_action:skip:{habit_id}")
    ]])
