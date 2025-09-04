from aiogram import Router, F
from aiogram.types import Message
from storage.db import async_session
from storage.models import Users, Sources

router = Router()

def register(dp): dp.include_router(router)

@router.message(F.text == "/sources")
async def cmd_sources(message: Message):
    async with async_session() as s:
        user = await Users.get_by_tg(s, message.from_user.id)
        if not user:
            await message.answer("Сначала /start")
            return
        srcs = await Sources.list_by_user(s, user.id, limit=8)
        if not srcs:
            await message.answer("Источники пока не добавлены. Сгенерируйте план: /plan")
            return
        txt = "<b>Последние источники:</b>\n" + "\n".join([f"• <a href='{x.url}'>{x.title or x.url}</a>" for x in srcs if x.url])
        await message.answer(txt)
