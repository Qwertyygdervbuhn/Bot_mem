from aiogram import Router
from handlers.meme import router as meme_router
from handlers.start import router as start_router


def setup_routers() -> Router:
    main_router = Router()
    main_router.include_router(start_router)
    main_router.include_router(meme_router)
    return main_router