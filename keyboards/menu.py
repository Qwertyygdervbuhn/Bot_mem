from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

BTN_CREATE_MEME = "🎨 Создать мем"
BTN_RANDOM_ROAST = "🎲 Рандомное ругательство"
BTN_ABOUT = "📖 О проекте"
BTN_BACK = "↩️ В главное меню"

BTN_POS_TOP = "⬆️ Сверху"
BTN_POS_CENTER = "⏺ Центр"
BTN_POS_BOTTOM = "⬇️ Снизу"


def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_CREATE_MEME)],
            [KeyboardButton(text=BTN_RANDOM_ROAST), KeyboardButton(text=BTN_ABOUT)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери действие на клавиатуре...",
    )


def get_back_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Нажми «В главное меню» для отмены...",
    )


def get_position_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BTN_POS_TOP),
                KeyboardButton(text=BTN_POS_CENTER),
                KeyboardButton(text=BTN_POS_BOTTOM),
            ],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери позицию текста...",
    )