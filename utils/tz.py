from zoneinfo import ZoneInfo, available_timezones
from config import DEFAULT_TZ as DEFAULT_TZ_ENV

DEFAULT_TZ = DEFAULT_TZ_ENV or "Asia/Almaty"

def valid_tz(name: str) -> bool:
    try:
        ZoneInfo(name)
        return True
    except Exception:
        return False
