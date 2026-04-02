from aiogram.dispatcher.router import Router

from tg_bot.routers import main_menu, habit_mark_completed

router = Router(name="main_app_router")
router.include_routers(
    main_menu.router,
    habit_mark_completed.router,
)
