import json
from aiogram import Router, F
from aiogram.types import Message
from storage.db import async_session
from storage.models import Users, Plans, Habits, Sources
from services.planner import plan_from_ai_json, habits_from_ai_json
from services.validation import clamp_duration
from ai.client import client_singleton

router = Router()

def register(dp): dp.include_router(router)

@router.message(F.text == "/plan")
async def cmd_plan(message: Message):
    async with async_session() as s:
        user = await Users.get_by_tg(s, message.from_user.id)
        if not user:
            await message.answer("Сначала /start")
            return
        profile = user.profile_json or {}
        msg = [
            {"role":"user","content": f"Профиль пользователя: {json.dumps(profile, ensure_ascii=False)}. "
             "Сформируй 3-недельный план. Если указано ограничение ≤30 мин/день — соблюдай."}
        ]
    data = await client_singleton.generate(msg)
    # Валидация и нормализация
    plan = plan_from_ai_json(data)
    # Создадим/сохраним
    async with async_session() as s:
        user = await Users.get_by_tg(s, message.from_user.id)
        p = await Plans.create(s, user_id=user.id, plan_json=plan)
        # Привычки
        habits = habits_from_ai_json(data)
        # По умолчанию ежедневные
        for h in habits:
            await Habits.create(
                s, user_id=user.id, title=h["title"],
                description=h.get("description",""),
                reminder_time=h.get("time","19:00"),
                days_mask="1111111", target_per_day=1, active=True
            )
        # Источники
        for src in data.get("sources", []):
            await Sources.create(s, user_id=user.id,
                                 title=src.get("title",""),
                                 url=src.get("url",""),
                                 summary="",)
        await s.commit()
    await message.answer(
        "Готово! План на 3 недели создан, привычки добавлены. Посмотреть привычки: /habits \n"
        "Источники: /sources \nЭкспорт: /export"
    )
