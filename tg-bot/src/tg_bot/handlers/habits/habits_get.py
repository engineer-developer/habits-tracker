
from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tg_bot.callbacks.user_profile import ProfileAction, ProfileMenuCallback
from tg_bot.keyboards.kb_factory import kb_habits_list
from tg_bot.services.api import ApiService
from tg_bot.services.redis import RedisService

router = Router(name="habit_list")


@router.callback_query(
    ProfileMenuCallback.filter(F.action == ProfileAction.habits_list),
)
async def get_non_completed_habit(
    callback: CallbackQuery,
    state: FSMContext,
    redis_service: RedisService,
    api_service: ApiService,
):
    """Обработчик callback получение всех не выполненных привычек."""
    token = await redis_service.get_token(telegram_id=callback.from_user.id)
    habits = await api_service.get_non_completed_habits(token)
    await callback.message.answer(
        text="Список привычек", reply_markup=kb_habits_list(habits=habits)
    )
