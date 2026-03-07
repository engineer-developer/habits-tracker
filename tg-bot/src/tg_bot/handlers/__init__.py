from aiogram.dispatcher.router import Router

from .auth import router as auth_router
from .main_menu import router as main_menu_router
from .habits import router as habit_router

router = Router(name="main_router")

router.include_routers(
    main_menu_router,
    auth_router,
    habit_router,
)
