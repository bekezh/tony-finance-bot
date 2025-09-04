import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from config import TG_TOKEN
from handlers import start, profile, plan, habits, reminders, sources, export
from services.scheduler import init_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zozh_bot")

async def main():
    if not TG_TOKEN:
        raise RuntimeError("TG_TOKEN is not set. Put it into .env")

    bot = Bot(TG_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Register handlers
    start.register(dp)
    profile.register(dp)
    plan.register(dp)
    habits.register(dp)
    reminders.register(dp)
    sources.register(dp)
    export.register(dp)

    # Start reminder scheduler
    await init_scheduler(bot)

    logging.info("Bot starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
