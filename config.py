import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./zozh.db")
DEFAULT_TZ = os.getenv("DEFAULT_TZ", "Asia/Almaty")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
REMINDERS_DEFAULT = os.getenv("REMINDERS_DEFAULT", "19:00")
