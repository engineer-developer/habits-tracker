import re
from datetime import time

from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.callbacks.habits import HabitAddConfirmAction, HabitAddConfirmCallback
from tg_bot.callbacks.user_profile import ProfileAction, ProfileMenuCallback
from tg_bot.configs.loguru_config import logger
from tg_bot.handlers.main_menu import show_user_profile
from tg_bot.keyboards.kb_factory import kb_habit_add_or_cancel
from tg_bot.schemas.habits import HabitCreateCommand, HabitJobCreateCommand
from tg_bot.services.api import ApiService
from tg_bot.services.redis import RedisService
from tg_bot.services.scheduler import SchedulerService
from tg_bot.states.states import HabitAddStates
from tg_bot.utils.notify import send_notify

router = Router(name="habit_add")


@router.callback_query(
    ProfileMenuCallback.filter(F.action == ProfileAction.habit_add),
)
async def add_habit(callback: CallbackQuery, state: FSMContext):
    """Обработчик callback добавления привычки."""
    await state.set_state(HabitAddStates.wait_for_habit_name)
    await callback.answer()
    await callback.message.answer(text="Отправьте название привычки.")


@router.message(HabitAddStates.wait_for_habit_name, F.text)
async def get_habit_name(message: Message, state: FSMContext):
    """Получение названия привычки."""
    title = message.text
    match = re.match(r"^[А-ЯЁа-яёA-Za-z0-9 \-:]+$", title)
    if not match:
        await message.answer(
            text="Используйте только буквы, цифры, пробел, дефис, двоеточие",
        )
        return

    logger.debug(f"Введено название привычки: {title}")
    await state.update_data(title=title)
    await state.set_state(HabitAddStates.wait_for_habit_description)
    await message.answer(text="Отправьте описание привычки.")


@router.message(HabitAddStates.wait_for_habit_description, F.text)
async def get_habit_description(message: Message, state: FSMContext):
    """Получение описания привычки."""
    description = message.text
    match = re.match(r"^[А-ЯЁа-яёA-Za-z0-9 \-:]+$", description)
    if not match:
        await message.answer(
            text="Используйте только буквы, цифры, пробел, дефис, двоеточие",
        )
        return

    logger.debug("Введено описание: {}", description)
    await state.update_data(description=description)
    await state.set_state(HabitAddStates.wait_for_habit_remind_time)
    await message.answer(
        text="Укажите время, в которое ежедневно будут приходить напоминания."
        "Например - 10:45"
    )


@router.message(HabitAddStates.wait_for_habit_remind_time, F.text)
async def get_habit_remind_time(message: Message, state: FSMContext):
    """Получение времени напоминания."""
    given_remind_time = message.text
    try:
        remind_time = time.fromisoformat(given_remind_time)
    except ValueError as exc:
        logger.error(f"Не верно указано время: {exc}")
        await message.answer(
            text="Не верно указано время. Укажите в формате: ЧЧ:ММ",
        )
        return

    logger.debug(f"Введено время: {remind_time}")
    await state.update_data(remind_time=remind_time.strftime("%H:%M:%S"))
    await state.set_state(HabitAddStates.wait_for_habit_remind_quantity)
    await message.answer(text="Сколько раз нужно напомнить?")


@router.message(HabitAddStates.wait_for_habit_remind_quantity, F.text)
async def get_habit_remind_quantity(message: Message, state: FSMContext):
    """Получение количества напоминаний."""
    given_remind_quantity = message.text
    try:
        remind_quantity = int(given_remind_quantity)
    except ValueError as exc:
        logger.error(f"Не верно указано количество: {exc}")
        await message.answer(
            text="Не верно указано количество. Введите только цифры",
        )
        return

    logger.debug("Введено количество: {}", remind_quantity)
    await state.update_data(remind_quantity=remind_quantity)

    habit_data = await state.get_data()
    logger.debug("Данные добавляемой привычки: {}", habit_data)
    await send_confirm_message(message, habit_data)


async def send_confirm_message(message: Message, habit_data: dict):
    """Отправка сообщения о добавляемой привычке."""
    text_parts = (
        f"Название привычки: *{habit_data.get('title')}*",
        f"Описание: *{habit_data.get('description')}*",
        f"Время напоминания: *{habit_data.get('remind_time')}*",
        f"Количество напоминаний: *{habit_data.get('remind_quantity')}*",
    )
    message_text = "\n".join(text_parts)
    await message.answer(
        text=message_text,
        parse_mode="Markdown",
        reply_markup=kb_habit_add_or_cancel(),
    )


@router.callback_query(
    HabitAddConfirmCallback.filter(F.action == HabitAddConfirmAction.add),
)
async def process_confirm_habit_add(
    callback: CallbackQuery,
    state: FSMContext,
    api_service: ApiService,
    redis_service: RedisService,
    scheduler_service: SchedulerService,
):
    """Обработка подтверждения добавления привычки."""
    async with ChatActionSender.typing(
        chat_id=callback.message.chat.id, bot=callback.bot
    ):
        token = await redis_service.get_token(telegram_id=callback.from_user.id)
        habit_data = await state.get_data()

        habit_create_cmd = habit_data.copy()
        habit_create_cmd.update(user_id=callback.from_user.id)
        habit = await api_service.habit_add(
            token=token,
            cmd=HabitCreateCommand.model_validate(habit_create_cmd),
        )
        if habit is None:
            logger.error("Привычка не добавлена.")
            rkb = ReplyKeyboardBuilder()
            rkb.button(text="/start")
            await callback.message.answer(
                text="Привычка не добавлена.", reply_markup=rkb.as_markup()
            )
            return

        job_create_cmd = habit_create_cmd.copy()
        job_create_cmd.update(habit_id=habit.id)
        job = await scheduler_service.create_job(
            func=send_notify,
            cmd=HabitJobCreateCommand.model_validate(job_create_cmd),
        )
        if not job:
            logger.error("Оповещение не запланировано.")
            return

        logger.debug(f"Добавлена привычка {habit.title}")
        await callback.answer()
        await callback.message.answer(f"Добавлена привычка '{habit.title}'")
        await state.clear()
        await show_user_profile(message=callback.message)


@router.callback_query(
    HabitAddConfirmCallback.filter(F.action == HabitAddConfirmAction.cancel),
)
async def process_cancel_habit_add(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Отмена добавления привычки."""
    logger.debug("Добавление привычки отменено.")
    await callback.answer(text="Добавление отменено")
    await state.clear()
    await show_user_profile(message=callback.message)
