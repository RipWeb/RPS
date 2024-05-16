from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    set_advert = State()
    set_greetings = State()
    set_channel = State()
    set_ref = State()
    set_mail = State()
    CheckSub = State()