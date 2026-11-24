from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.menu import BTN_ABOUT, BTN_BACK, BTN_RANDOM_ROAST, get_main_keyboard
from services import get_random_roast

router = Router()

MAIN_MENU_TEXT = (
    "<b>БИТВА ФРАЗ</b> — студия мемов\n\n"
    "Собери картинку с подписью или выбей случайную связку из двух слов.\n\n"
    "Выбери действие на клавиатуре ниже:"
)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    name = (
        message.from_user.first_name
        if message.from_user and message.from_user.first_name
        else "игрок"
    )
    text = f"Привет, <b>{name}</b>!\n\n{MAIN_MENU_TEXT}"
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")


@router.message(F.text == BTN_RANDOM_ROAST)
async def msg_random_roast(message: Message):
    roast = get_random_roast()
    await message.answer(
        f"🎲 <b>Выпало:</b> <b>{roast}</b>",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == BTN_ABOUT)
async def msg_about(message: Message):
    about_text = (
        "<b>О проекте «Битва фраз»</b>\n\n"
        "Генератор мемов с выбором позиции текста и генератор случайных связок из двух слов.\n\n"
        "<i>Проект в активной разработке.</i>"
    )
    await message.answer(about_text, reply_markup=get_main_keyboard(), parse_mode="HTML")


@router.message(F.text == BTN_BACK)
async def msg_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(MAIN_MENU_TEXT, reply_markup=get_main_keyboard(), parse_mode="HTML")