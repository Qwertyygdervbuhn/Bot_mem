import os
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# ТОКЕН БОТА
TOKEN = "9134067477:AAHBYq2pIVSzVCePk2hriZBD6ne3lAlHPWU"

bot = Bot(token=TOKEN)
router = Router()


# Состояния FSM (заглушка для будущих разделов меню)
class MenuState(StatesGroup):
    in_sub_menu = State()


# --- КЛАВИАТУРЫ МЕНЮ ---
def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=" Создать мем", callback_data="create_meme")],
            [InlineKeyboardButton(text="ℹ О боте", callback_data="about")],
        ]
    )


def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад в меню", callback_data="cancel")]]
    )


# --- ОБРАБОТЧИКИ КОМАНД И МЕНЮ ---
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я — бот **Битва фраз**. Главное меню готово к работе.\n\n"
        "Выбери действие в меню ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")


@router.callback_query(F.data == "about")
async def callback_about(callback: CallbackQuery):
    about_text = (
        "ℹ️ **О боте 'Битва фраз':**\n\n"
        "Это базовый каркас бота,бот в разработке."
    )
    await callback.message.edit_text(about_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def callback_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Главное меню:", reply_markup=get_main_keyboard())
    await callback.answer()


# --- ЗАГЛУШКА ДЛЯ РАЗДЕЛА СОЗДАНИЯ МЕМА ---
@router.callback_query(F.data == "create_meme")
async def callback_create_meme(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        " Раздел создания мемов находится в разработке.\n\nЗдесь будет выбор параметров генерации.",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


# --- ЗАПУСК БОТА ---
async def main():
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот 'Битва фраз' (только меню) запущен...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())