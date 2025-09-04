from aiogram.fsm.state import State, StatesGroup

class Onboarding(StatesGroup):
    goal = State()
    limits = State()
    prefs = State()
    schedule = State()
    location = State()
    result_format = State()
    confirm = State()
