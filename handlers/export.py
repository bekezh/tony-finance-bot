import json, io, csv, datetime
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from storage.db import async_session
from storage.models import Users, Plans, Habits, HabitLogs, Sources
from services.pdf import make_plan_pdf

router = Router()

def register(dp): dp.include_router(router)

@router.message(F.text == "/export")
async def cmd_export(message: Message):
    async with async_session() as s:
        user = await Users.get_by_tg(s, message.from_user.id)
        if not user:
            await message.answer("Сначала /start")
            return
        plan = await Plans.last_by_user(s, user.id)
        habits = await Habits.list_active_by_user(s, user.id)
        logs = await HabitLogs.list_by_user(s, user.id)
        srcs = await Sources.list_by_user(s, user.id, limit=100)

    # JSON export
    payload = {
        "profile": user.profile_json or {},
        "plan": plan.plan_json if plan else {},
        "habits": [{"title":h.title,"time":h.reminder_time,"days_mask":h.days_mask} for h in habits],
        "sources": [{"title":t.title,"url":t.url,"summary":t.summary} for t in srcs],
        "exported_at": datetime.datetime.utcnow().isoformat()+"Z"
    }
    json_bytes = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    json_file = io.BytesIO(json_bytes); json_file.name = "export.json"

    # CSV logs
    csv_buf = io.StringIO()
    writer = csv.writer(csv_buf)
    writer.writerow(["date","habit_title","status"])
    for l in logs:
        writer.writerow([l.date.isoformat(), l.habit.title if l.habit else "", l.status])
    csv_bytes = csv_buf.getvalue().encode("utf-8")
    csv_file = io.BytesIO(csv_bytes); csv_file.name = "habit_logs.csv"

    # PDF
    pdf_bytes = make_plan_pdf(user, plan, habits)
    pdf_file = io.BytesIO(pdf_bytes); pdf_file.name = "plan.pdf"

    await message.answer_document(FSInputFile(json_file), caption="JSON экспорт")
    await message.answer_document(FSInputFile(csv_file), caption="CSV логи")
    await message.answer_document(FSInputFile(pdf_file), caption="PDF план")
