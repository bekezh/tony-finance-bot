from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.onboarding import kb_disclaimer, kb_onboarding_start
from storage.db import async_session
from storage.models import Users
from utils.tz import DEFAULT_TZ

router = Router()

def register(dp): dp.include_router(router)

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я ЗОЖ-коуч.\n\n<b>Дисклеймер:</b> я не врач. "
        "Рекомендации носят информационный характер. "
        "При заболеваниях — к врачу.",
        reply_markup=kb_disclaimer()
    )

@router.callback_query(F.data == "agree_disclaimer")
async def agree(cb: CallbackQuery):
    # upsert user
    async with async_session() as s:
        user = await Users.get_or_create(s, tg_id=cb.from_user.id, tz=DEFAULT_TZ, consent=True)
        await s.commit()
    await cb.message.edit_text(
        "Отлично. Давайте начнём с короткого опроса: кто вы и чего хотите достичь?",
        reply_markup=kb_onboarding_start()
    )
