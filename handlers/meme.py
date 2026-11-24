import asyncio
import io

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from keyboards.menu import (
    BTN_BACK,
    BTN_CREATE_MEME,
    BTN_POS_BOTTOM,
    BTN_POS_CENTER,
    BTN_POS_TOP,
    get_back_keyboard,
    get_main_keyboard,
    get_position_keyboard,
)
from services import create_meme_image
from states import MemeCreationState

router = Router()

POS_TEXT_MAP = {
    BTN_POS_TOP: ("top", "сверху"),
    BTN_POS_CENTER: ("center", "по центру"),
    BTN_POS_BOTTOM: ("bottom", "снизу"),
}


@router.message(F.text == BTN_CREATE_MEME)
async def start_create_meme(message: Message, state: FSMContext):
    await state.set_state(MemeCreationState.waiting_for_photo)
    await message.answer(
        "<b>Шаг 1 из 3 — Фотография</b>\n\n"
        "Отправь фото, на котором нужно разместить подпись.",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )


@router.message(MemeCreationState.waiting_for_photo, F.text == BTN_BACK)
@router.message(MemeCreationState.waiting_for_position, F.text == BTN_BACK)
@router.message(MemeCreationState.waiting_for_caption, F.text == BTN_BACK)
async def back_during_creation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Создание мема отменено. Главное меню:",
        reply_markup=get_main_keyboard(),
    )


@router.message(MemeCreationState.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext, bot: Bot):
    if not message.photo:
        return
    photo = message.photo[-1]
    buffer = io.BytesIO()
    await bot.download(photo, destination=buffer)

    await state.update_data(photo_bytes=buffer.getvalue())
    await state.set_state(MemeCreationState.waiting_for_position)

    await message.answer(
        "<b>Шаг 2 из 3 — Позиция текста</b>\n\n"
        "Фото получено. Выбери, где расположить подпись:",
        reply_markup=get_position_keyboard(),
        parse_mode="HTML",
    )


@router.message(MemeCreationState.waiting_for_photo)
async def process_photo_invalid(message: Message):
    await message.answer(
        "Нужна именно <b>фотография</b> — текст или стикер сюда не подойдут.",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )


@router.message(
    MemeCreationState.waiting_for_position,
    F.text.in_(POS_TEXT_MAP.keys()),
)
async def process_position(message: Message, state: FSMContext):
    if not message.text:
        return
    position_key, position_label = POS_TEXT_MAP[message.text]

    await state.update_data(text_position=position_key)
    await state.set_state(MemeCreationState.waiting_for_caption)

    await message.answer(
        f"<b>Шаг 3 из 3 — Подпись</b>\n\n"
        f"Позиция: <b>{position_label}</b>.\n"
        "Теперь отправь текст, который нужно наложить на фото:",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )


@router.message(MemeCreationState.waiting_for_position)
async def process_position_invalid(message: Message):
    await message.answer(
        "Выбери позицию текста на клавиатуре ниже:",
        reply_markup=get_position_keyboard(),
    )


@router.message(MemeCreationState.waiting_for_caption, F.text)
async def process_caption(message: Message, state: FSMContext):
    if not message.text:
        return
    caption = message.text.strip()
    if not caption:
        await message.answer(
            "Текст пустой. Напиши фразу для мема:",
            reply_markup=get_back_keyboard(),
        )
        return

    data = await state.get_data()
    photo_bytes = data.get("photo_bytes")
    position = data.get("text_position", "bottom")

    if not photo_bytes:
        await state.set_state(MemeCreationState.waiting_for_photo)
        await message.answer(
            "Фото не найдено в текущей сессии. Отправь фотографию заново:",
            reply_markup=get_back_keyboard(),
        )
        return

    result_bytes = await asyncio.to_thread(
        create_meme_image, photo_bytes, caption, position
    )
    await state.clear()

    result_file = BufferedInputFile(result_bytes, filename="meme.png")
    await message.answer_photo(
        photo=result_file,
        caption="<b>Готово!</b> Твой мем собран.",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML",
    )


@router.message(MemeCreationState.waiting_for_caption)
async def process_caption_invalid(message: Message):
    await message.answer(
        "Отправь подпись <b>текстовым сообщением</b>.",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )