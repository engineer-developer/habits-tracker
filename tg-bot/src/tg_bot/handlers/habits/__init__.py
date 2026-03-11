from aiogram.dispatcher.router import Router
from .habit_add import router as habit_add_router
from .habit_mark_completed import router as habit_mark_completed_router
from .habits_get import router as habits_list_router

router = Router(name="habit")

router.include_router(habit_add_router)
router.include_router(habit_mark_completed_router)
router.include_router(habits_list_router)
