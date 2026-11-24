from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    in_sub_menu = State()


class MemeCreationState(StatesGroup):
    waiting_for_photo = State()
    waiting_for_position = State()
    waiting_for_caption = State()