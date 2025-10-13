from telebot.states import State, StatesGroup
from telebot.storage import StateMemoryStorage

class AuthStates(StatesGroup):
    wait_password = State()


state_storage = StateMemoryStorage()