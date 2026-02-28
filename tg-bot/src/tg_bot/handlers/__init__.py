from aiogram.dispatcher.router import Router

from .auth import router as auth_router
from .main_menu import router as main_menu_router

router = Router(name="main")

router.include_router(main_menu_router)
router.include_router(auth_router)
