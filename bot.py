import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TG_TOKEN
from handlers import start, profile, plan, habits, reminders, sources, export
from services.scheduler import init_scheduler
from storage.db import init_models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zozh_bot")

async def main():
    if not TG_TOKEN:
        raise RuntimeError("TG_TOKEN is not set. Put it into .env")

    # aiogram >= 3.7: use DefaultBotProperties instead of parse_mode kwarg
    bot = Bot(TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Register handlers
    start.register(dp)
    profile.register(dp)
    plan.register(dp)
    habits.register(dp)
    reminders.register(dp)
    sources.register(dp)
    export.register(dp)

    # Create DB tables before starting scheduler
    await init_models()

    # Start reminder scheduler
    await init_scheduler(bot)

    logging.info("Bot starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
