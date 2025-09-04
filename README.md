# ZOZH Coach Bot (aiogram 3)

Телеграм-бот ИИ-коуч по ЗОЖ: онбординг → диалог/проверка → оформление плана (3 недели), привычки, напоминания, экспорт PDF/CSV/JSON.

**Стек:** Python 3.11+, aiogram 3.x, SQLAlchemy 2.x, APScheduler, ReportLab, OpenAI (через абстрактный слой).  
**TZ по умолчанию:** Asia/Almaty (UTC+5).

## Быстрый старт (локально)

1) Установите Python 3.11+.
2) Склонируйте/распакуйте проект и установите зависимости:
   ```bash
   python -m venv .venv
   . .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3) Скопируйте `.env.example` ⇒ `.env` и заполните переменные:
   - `TG_TOKEN` — токен вашего Telegram-бота
   - `OPENAI_API_KEY` — ключ OpenAI (опционально; без него вернётся демо-ответ)
   - `DATABASE_URL` — по умолчанию SQLite `sqlite+aiosqlite:///./zozh.db`
   - `DEFAULT_TZ` — `Asia/Almaty`
4) Запустите бота:
   ```bash
   python bot.py
   ```

> Запуск использует **long polling**. Для продакшна можно оставить polling (проще) или настроить webhook.

## Структура
```
zozh_coach_bot/
├─ bot.py
├─ config.py
├─ requirements.txt
├─ .env.example
├─ ai/
│  ├─ client.py
│  └─ prompts.py
├─ handlers/
│  ├─ __init__.py
│  ├─ start.py
│  ├─ profile.py
│  ├─ plan.py
│  ├─ habits.py
│  ├─ reminders.py
│  ├─ sources.py
│  └─ export.py
├─ keyboards/
│  ├─ __init__.py
│  ├─ onboarding.py
│  ├─ dialog.py
│  └─ tracking.py
├─ fsm/
│  ├─ __init__.py
│  ├─ onboarding.py
│  └─ dialog.py
├─ services/
│  ├─ __init__.py
│  ├─ planner.py
│  ├─ pdf.py
│  ├─ scheduler.py
│  └─ validation.py
├─ storage/
│  ├─ __init__.py
│  ├─ db.py
│  └─ models.py
├─ utils/
│  ├─ __init__.py
│  ├─ tz.py
│  └─ logging.py
└─ docker/
   ├─ Dockerfile
   └─ docker-compose.yml
```

## Команды
- `/start` — приветствие, дисклеймер, запуск онбординга.
- `/profile` — просмотр/редактирование анкеты и TZ.
- `/plan` — сгенерировать/обновить 3-недельный план (через ИИ).
- `/habits` — список привычек и быстрые отметки.
- `/reminders [HH:MM]` — время уведомлений (по умолчанию 19:00).
- `/sources` — последние источники/проверки.
- `/export` — экспорт PDF/CSV/JSON.
- `/help` — справка.

## Экспорт
- **PDF**: план на 3 недели + карточки привычек.
- **CSV**: логи привычек (дата, статус).
- **JSON**: профиль + план + привычки + источники.

## 24/7 деплой (варианты)

### Docker Compose (VPS)
1) Заполните `.env`.
2) Запустите:
   ```bash
   docker compose -f docker/docker-compose.yml up -d --build
   ```
3) Для автообновлений используйте watchtower или CI/CD.

### Railway/Render/Fly.io
- Соберите образ из `docker/Dockerfile` и задайте переменные окружения.
- Откройте исходящий трафик (Telegram) и убедитесь, что контейнер имеет корректную TZ.

### Systemd (polling)
- Создайте сервис-файл, активируйте venv и команду `python bot.py`.
- Добавьте `Restart=always` и логирование в journald.

## Тест-кейсы минимум
- Онбординг без роста/веса — не блокируем продолжение.
- «Нет бассейна» → план без плавания.
- URL для резюме — честно просим текст, если не можем открыть.
- ≤30 мин/день соблюдается при генерации.
- Напоминания приходят по TZ Asia/Almaty.
- Экспорт работает.

## Лицензия
MIT • 2025-09-04
