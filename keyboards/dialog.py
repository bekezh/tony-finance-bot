from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_dialog_filters():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Исключить", callback_data="dlg:exclude"),
         InlineKeyboardButton(text="Заменить", callback_data="dlg:replace")],
        [InlineKeyboardButton(text="Пояснить термин", callback_data="dlg:term"),
         InlineKeyboardButton(text="Проверить источник", callback_data="dlg:source")],
        [InlineKeyboardButton(text="Резюме по ссылке", callback_data="dlg:summary")]
    ])
