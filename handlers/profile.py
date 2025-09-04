import json
from aiogram import Router, F
from aiogram.types import Message
from storage.db import async_session
from storage.models import Users
from utils.tz import valid_tz, DEFAULT_TZ

router = Router()

def register(dp): dp.include_router(router)

@router.message(F.text == "/profile")
async def cmd_profile(message: Message):
    async with async_session() as s:
        user = await Users.get_by_tg(s, message.from_user.id)
        if not user:
            await message.answer("Профиль не найден. Нажмите /start")
            return
        profile = user.profile_json or {}
        tz = user.tz or DEFAULT_TZ
        txt = "<b>Ваш профиль</b>\n— TZ: {}\n— Consent: {}\n— Данные: <code>{}</code>".format(
            tz, "yes" if user.consent else "no", json.dumps(profile, ensure_ascii=False)
        )
        await message.answer(txt)

@router.message(F.text.regexp(r"^/profile_tz\s+(.+)$"))
async def set_tz(message: Message):
    tz_name = message.text.split(maxsplit=1)[1].strip()
    if not valid_tz(tz_name):
        await message.answer("Неверная TZ. Пример: <code>Asia/Almaty</code>")
        return
    async with async_session() as s:
        user = await Users.get_by_tg(s, message.from_user.id)
        if not user:
            await message.answer("Сначала /start")
            return
        user.tz = tz_name
        await s.commit()
    await message.answer(f"Часовой пояс обновлён: <b>{tz_name}</b>")

@router.message(F.text.startswith("/help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Помощь</b>\n"
        "/start — онбординг\n"
        "/profile — профиль\n"
        "/profile_tz Asia/Almaty — установить TZ\n"
        "/plan — сгенерировать план\n"
        "/habits — привычки\n"
        "/reminders HH:MM — установить время напоминаний\n"
        "/sources — источники\n"
        "/export — экспорт PDF/CSV/JSON"
    )
