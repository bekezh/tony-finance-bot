from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_disclaimer():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Согласен", callback_data="agree_disclaimer")
    ]])

def kb_onboarding_start():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Начать онбординг", callback_data="ob_start")
    ]])
