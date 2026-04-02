import typing
from datetime import time

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import ScenesManager, on
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from tg_bot import callbacks, keyboards, schemas, services
from tg_bot import scenes as app_scenes
from tg_bot.configs.loguru_config import logger
from tg_bot.routers.habit_mark_completed import habit_mark_completed
from tg_bot.scenes import mixins
from tg_bot.utils import notify

not_back_or_cancel_data_filter = F.data.not_in({"back", "cancel"})


class AddHabitTitleInputScene(
    app_scenes.CancellableScene,
    mixins.ValidateTitleMixin,
    state="input_habit_title",
):
    """Сцена ввода названия привычки."""

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery) -> None:
        await callback_query.message.edit_text(
            text="Введите название привычки...", reply_markup=keyboards.kb_back_cancel()
        )

    @on.message(F.text)
    async def get_title(self, message: Message, state: FSMContext):
        title = await self.validate_title(message=message)
        if title is None:
            return
        habit_info = dict(title=title)
        await state.update_data(habit_info=habit_info)
        await self.wizard.goto(AddHabitDescriptionInputScene)


class AddHabitDescriptionInputScene(
    app_scenes.CancellableScene,
    mixins.ValidateDescriptionMixin,
    state="input_habit_description",
):
    """Сцена ввода описания привычки."""

    @on.message.enter()
    async def on_enter(self, message: Message):
        await message.answer(
            text="Введите описание привычки...",
            reply_markup=keyboards.kb_back_cancel(),
        )

    @on.message(F.text)
    async def get_description(self, message: Message, state: FSMContext):
        description = await self.validate_description(message=message)
        if description is None:
            return
        habit_info: dict = await state.get_value("habit_info")
        habit_info.update(description=description)
        await state.update_data(habit_info=habit_info)
        await self.wizard.goto(AddHabitRemindTimeInputScene)


class AddHabitRemindTimeInputScene(
    app_scenes.CancellableScene,
    mixins.ValidateRemindTimeMixin,
    state="input_habit_remind_time",
):
    """Сцена ввода времени напоминания привычки."""

    @on.message.enter()
    async def on_enter(self, message: Message):
        await message.answer(
            text="Укажите время, в которое ежедневно будут приходить напоминания."
            "Например - 10:45",
            reply_markup=keyboards.kb_back_cancel(),
        )

    @on.message(F.text)
    async def get_remind_time(self, message: Message, state: FSMContext):
        remind_time = await self.validate_remind_time(message=message)
        if remind_time is None:
            return
        habit_info: dict = await state.get_value("habit_info")
        habit_info.update(remind_time=remind_time)
        await state.update_data(habit_info=habit_info)
        await self.wizard.goto(AddHabitRemindQuantityInputScene)


class AddHabitRemindQuantityInputScene(
    app_scenes.CancellableScene,
    mixins.ValidateRemindQuantityMixin,
    state="input_habit_remind_quantity",
):
    """Сцена ввода количества напоминаний привычки."""

    @on.message.enter()
    async def on_enter(self, message: Message):
        await message.answer(
            text="Сколько раз нужно напомнить?",
            reply_markup=keyboards.kb_back_cancel(),
        )

    @on.message(F.text)
    async def get_remind_quantity(self, message: Message, state: FSMContext):
        remind_quantity = await self.validate_remind_quantity(message=message)
        if remind_quantity is None:
            return
        habit_info: dict = await state.get_value("habit_info")
        habit_info.update(remind_quantity=remind_quantity)
        await state.update_data(habit_info=habit_info)
        await self.wizard.goto(AddHabitConfirmScene)


class AddHabitConfirmScene(app_scenes.CancellableScene, state="habit_confirm_add"):
    """Сцена подтверждения или отмены добавления привычки."""

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext):
        habit_info: dict = await state.get_value("habit_info")
        text_parts = (
            f"Название привычки: {habit_info.get('title')}",
            f"Описание: {habit_info.get('description')}",
            f"Время напоминания: {habit_info.get('remind_time')}",
            f"Количество напоминаний: {habit_info.get('remind_quantity')}",
        )
        message_text = "\n".join(text_parts)
        await message.answer(
            text=message_text,
            parse_mode="Markdown",
            reply_markup=keyboards.kb_habit_add_or_cancel(),
        )

    @on.callback_query(
        callbacks.HabitAddConfirmActionCallback.filter(
            F.action == callbacks.HabitAddConfirmAction.add
        ),
    )
    async def process_habit_add_confirm(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        api_service: services.ApiService,
        redis_service: services.RedisService,
        scheduler_service: services.SchedulerService,
    ):
        """Обработка подтверждения добавления привычки."""
        async with ChatActionSender.typing(
            chat_id=callback.message.chat.id, bot=callback.bot
        ):
            token = await redis_service.get_token(telegram_id=callback.from_user.id)
            habit_info: dict = await state.get_value("habit_info")
            habit_info.update(user_id=callback.from_user.id)
            habit = await api_service.create_habit(
                token=token,
                cmd=schemas.HabitCreateCommand.model_validate(habit_info),
            )
            if habit is None:
                err_msg = "Привычка не добавлена."
                logger.error(err_msg)
                await callback.answer(text=err_msg)
                return await self.wizard.goto(app_scenes.MainMenuScene)

            job_create_cmd = habit_info.copy()
            job_create_cmd.update(habit_id=habit.id)
            job = await scheduler_service.create_job(
                func=notify.send_notify,
                cmd=schemas.HabitJobCreateCommand.model_validate(job_create_cmd),
            )
            if job is None:
                logger.error("Оповещение не запланировано.")
                return

            logger.debug(f"Добавлена привычка {habit.title}")
            await callback.answer()
            await callback.message.answer(f"Добавлена привычка '{habit.title}'")
            await self.wizard.goto(app_scenes.MainMenuScene)

    @on.callback_query(
        callbacks.HabitAddConfirmActionCallback.filter(
            F.action == callbacks.HabitAddConfirmAction.cancel
        ),
    )
    async def process_cancel_habit_add(
        self,
        callback: CallbackQuery,
    ):
        """Отмена добавления привычки."""
        logger.debug("Добавление привычки отменено.")
        await callback.answer(text="Добавление отменено")
        await self.wizard.goto(app_scenes.MainMenuScene)


class ActiveHabitsScene(app_scenes.CancellableScene, state="menu_active_habits"):
    """Сцена со списком активных привычек."""

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
        redis_service: services.RedisService,
        api_service: services.ApiService,
    ) -> None:
        token = await redis_service.get_token(telegram_id=callback_query.from_user.id)
        habits = await api_service.get_non_completed_habits(token)
        if habits is None:
            await callback_query.message.edit_text(
                text="Нет активных привычек.",
                reply_markup=keyboards.kb_back_cancel(),
            )
            return

        await callback_query.message.edit_text(
            text="Список активных привычек",
            reply_markup=keyboards.kb_active_habits(habits=habits),
        )

    @on.callback_query(not_back_or_cancel_data_filter)
    async def get_habit_details(
        self,
        callback_query: CallbackQuery,
        state: FSMContext,
        api_service: services.ApiService,
    ):
        async with ChatActionSender.typing(
            chat_id=callback_query.message.chat.id, bot=callback_query.bot, interval=1
        ):
            habit_id = int(callback_query.data.rsplit(":", maxsplit=1)[-1])
            habit = await api_service.get_habit_by_id(
                query=schemas.HabitByIdQuery(id=habit_id)
            )
            if habit is None:
                await callback_query.answer("Нет удалось получить информацию")
                return

            await state.update_data(habit=habit.model_dump(mode="json"))
            await callback_query.answer()
            await self.wizard.goto(HabitDetailsScene)


class CompletedHabitsScene(app_scenes.CancellableScene, state="menu_completed_habits"):
    """Сцена со списком завершенных привычек."""

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
        redis_service: services.RedisService,
        api_service: services.ApiService,
    ) -> None:
        token = await redis_service.get_token(telegram_id=callback_query.from_user.id)
        habits = await api_service.get_completed_habits(token)
        if not habits:
            await callback_query.message.edit_text(
                text="Нет завершенных привычек.",
                reply_markup=keyboards.kb_back_cancel(),
            )
            return

        await callback_query.message.edit_text(
            text="Список завершенных привычек",
            reply_markup=keyboards.kb_completed_habits(habits=habits),
        )

    @on.callback_query(F.data == "clear_completed_habits")
    async def clear_completed_habits(
        self,
        callback_query: CallbackQuery,
        api_service: services.ApiService,
        redis_service: services.RedisService,
    ):
        token = await redis_service.get_token(telegram_id=callback_query.from_user.id)
        await api_service.delete_completed_habits(token=token)
        await callback_query.answer("Завершенные привычки удалены")
        await callback_query.message.delete()
        await self.wizard.back()

    @on.callback_query(F.data.startswith("habit_id"))
    async def answer_on_button_click(self, callback_query: CallbackQuery):
        logger.debug(f"No action on this button\ncb_data: {callback_query.data}")
        await callback_query.answer("No action")


class HabitDetailsScene(app_scenes.CancellableScene, state="menu_habit_details"):
    """Сцена информации о привычке.

    Есть кнопки 'выполнить', 'изменить', 'удалить'.
    """

    async def get_habit_info(self, habit: schemas.HabitRead) -> str:
        """Формирует строку с информацией о привычке."""
        habit_info = (
            f"Название: {habit.title}\n"
            f"Описание: {habit.description.capitalize()}\n"
            f"Время оповещения: {habit.remind_time}\n"
            f"Статус: {'выполнено' if habit.completed else 'не выполнено'}\n"
            f"Статистика выполнений: {len(habit.tracking)} из {habit.remind_quantity}"
        )
        return habit_info

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
        state: FSMContext,
    ) -> None:
        habit = schemas.HabitRead.model_validate(await state.get_value("habit"))
        habit_info = await self.get_habit_info(habit)
        await callback_query.answer()
        await callback_query.message.edit_text(
            text=habit_info,
            reply_markup=keyboards.kb_habit_edit_delete_complete(habit_id=habit.id),
        )

    @on.callback_query(
        callbacks.HabitDetailsActionCallback.filter(
            F.action == callbacks.HabitDetailsAction.habit_complete
        )
    )
    async def goto_habit_mark_completed(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.wizard.goto(app_scenes.HabitMarkCompletedScene)

    @on.callback_query(
        callbacks.HabitDetailsActionCallback.filter(
            F.action == callbacks.HabitDetailsAction.habit_edit
        )
    )
    async def goto_habit_edit(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.wizard.goto(app_scenes.HabitEditScene)

    @on.callback_query(
        callbacks.HabitDetailsActionCallback.filter(
            F.action == callbacks.HabitDetailsAction.habit_delete
        )
    )
    async def goto_habit_delete(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.wizard.goto(app_scenes.HabitDeleteScene)


class HabitMarkCompletedScene(
    app_scenes.CancellableScene, state="menu_habit_mark_completed"
):
    """Сцена для регистрации факта выполнения привычки."""

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
        scenes: ScenesManager,
        api_service: services.ApiService,
        redis_service: services.RedisService,
        scheduler_service: services.SchedulerService,
    ):
        """Фиксирует факт выполнения привычки."""

        await habit_mark_completed(
            callback_query=callback_query,
            scenes=scenes,
            api_service=api_service,
            redis_service=redis_service,
            scheduler_service=scheduler_service,
        )


class HabitEditScene(app_scenes.CancellableScene, state="menu_habit_edit"):
    """Сцена редактирования привычки.

    Показывает сообщение с кнопками того, что нужно изменить.
    """

    @on.callback_query.enter()
    async def on_callback_enter(
        self,
        callback_query: CallbackQuery,
        state: FSMContext,
    ):
        habit = schemas.HabitRead.model_validate(await state.get_value("habit"))
        await callback_query.message.edit_text(
            text="Что нужно изменить?",
            reply_markup=keyboards.kb_habit_edit_choices(habit_id=habit.id),
        )

    @on.callback_query(
        callbacks.HabitEditActionCallback.filter(
            F.action == callbacks.HabitEditAction.habit_title
        )
    )
    async def goto_edit_habit_title(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.wizard.goto(app_scenes.HabitUpdateTitleScene)

    @on.callback_query(
        callbacks.HabitEditActionCallback.filter(
            F.action == callbacks.HabitEditAction.habit_description
        )
    )
    async def goto_edit_habit_description(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.wizard.goto(app_scenes.HabitUpdateDescriptionScene)

    @on.callback_query(
        callbacks.HabitEditActionCallback.filter(
            F.action == callbacks.HabitEditAction.remind_time
        )
    )
    async def goto_edit_habit_remind_time(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.wizard.goto(app_scenes.HabitUpdateRemindTimeScene)

    @on.callback_query(
        callbacks.HabitEditActionCallback.filter(
            F.action == callbacks.HabitEditAction.remind_quantity
        )
    )
    async def goto_edit_habit_remind_quantity(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.wizard.goto(app_scenes.HabitUpdateRemindQuantityScene)


class HabitUpdateTitleScene(
    app_scenes.CancellableScene,
    mixins.ValidateTitleMixin,
    state="habit_update_title",
):
    """Сцена обновления названия привычки."""

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
    ):
        await callback_query.message.edit_text(
            text="Введите название...",
            reply_markup=keyboards.kb_cancel(),
        )

    @on.message(F.text)
    async def update_title(
        self,
        message: Message,
        state: FSMContext,
        redis_service: services.RedisService,
        api_service: services.ApiService,
    ):
        """Обновление названия привычки."""
        title = await self.validate_title(message=message)
        if title is None:
            return

        token = await redis_service.get_token(telegram_id=message.from_user.id)
        state_data = await state.get_data()
        current_habit = schemas.HabitRead.model_validate(state_data.get("habit"))
        edited_habit = await api_service.update_habit(
            token=token,
            habit_id=current_habit.id,
            cmd=schemas.HabitUpdateCommand(title=title),
        )
        await message.answer(
            text=f"Название привычки изменено на '{edited_habit.title}'"
        )
        await self.wizard.goto(app_scenes.MainMenuScene)


class HabitUpdateDescriptionScene(
    app_scenes.CancellableScene,
    mixins.ValidateDescriptionMixin,
    state="habit_update_description",
):
    """Сцена обновления описания привычки."""

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
    ):
        await callback_query.message.edit_text(
            text="Введите описание...",
            reply_markup=keyboards.kb_cancel(),
        )

    @on.message(F.text)
    async def update_description(
        self,
        message: Message,
        state: FSMContext,
        redis_service: services.RedisService,
        api_service: services.ApiService,
    ):
        """Обновление описания привычки."""
        description = await self.validate_description(message=message)
        if description is None:
            return

        token = await redis_service.get_token(telegram_id=message.from_user.id)
        state_data = await state.get_data()
        current_habit = schemas.HabitRead.model_validate(state_data.get("habit"))
        edited_habit = await api_service.update_habit(
            token=token,
            habit_id=current_habit.id,
            cmd=schemas.HabitUpdateCommand(description=description),
        )
        await message.answer(
            text=f"Описание привычки изменено на '{edited_habit.description}'"
        )
        await self.wizard.goto(app_scenes.MainMenuScene)


class HabitUpdateRemindTimeScene(
    app_scenes.CancellableScene,
    mixins.ValidateRemindTimeMixin,
    state="habit_update_remind_time",
):
    """Сцена обновления времени напоминания."""

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
    ):
        await callback_query.message.edit_text(
            text="Введите время напоминания...",
            reply_markup=keyboards.kb_cancel(),
        )

    @on.message(F.text)
    async def update_remind_time(
        self,
        message: Message,
        state: FSMContext,
        redis_service: services.RedisService,
        api_service: services.ApiService,
        scheduler_service: services.SchedulerService,
    ):
        """Обновление времени напоминания."""
        remind_time = await self.validate_remind_time(message=message)
        if remind_time is None:
            return

        token = await redis_service.get_token(telegram_id=message.from_user.id)
        state_data = await state.get_data()
        current_habit = schemas.HabitRead.model_validate(state_data.get("habit"))
        edited_habit = await api_service.update_habit(
            token=token,
            habit_id=current_habit.id,
            cmd=schemas.HabitUpdateCommand(remind_time=time.fromisoformat(remind_time)),
        )
        await scheduler_service.edit_job_schedule_time(
            job_id=edited_habit.id,
            remind_time=edited_habit.remind_time,
        )
        await message.answer(
            text=f"Время напоминания изменено на {edited_habit.remind_time}"
        )
        await self.wizard.goto(app_scenes.MainMenuScene)


class HabitUpdateRemindQuantityScene(
    app_scenes.CancellableScene,
    mixins.ValidateRemindQuantityMixin,
    state="habit_update_remind_quantity",
):
    """Сцена обновления количества напоминаний."""

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
    ):
        await callback_query.message.edit_text(
            text="Введите количество напоминаний...",
            reply_markup=keyboards.kb_cancel(),
        )

    @on.message(F.text)
    async def update_remind_quantity(
        self,
        message: Message,
        state: FSMContext,
        redis_service: services.RedisService,
        api_service: services.ApiService,
    ):
        """Обновление количества напоминаний."""
        remind_quantity = await self.validate_remind_quantity(message=message)
        if remind_quantity is None:
            return

        token = await redis_service.get_token(telegram_id=message.from_user.id)
        state_data = await state.get_data()
        current_habit = schemas.HabitRead.model_validate(state_data.get("habit"))
        edited_habit = await api_service.update_habit(
            token=token,
            habit_id=current_habit.id,
            cmd=schemas.HabitUpdateCommand(remind_quantity=remind_quantity),
        )
        await message.answer(
            text=f"Количество напоминаний изменено на {edited_habit.remind_quantity}"
        )
        await self.wizard.goto(app_scenes.MainMenuScene)


class HabitDeleteScene(app_scenes.CancellableScene, state="menu_habit_delete"):
    """Сцена для удаления привычки."""

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
        api_service: services.ApiService,
        redis_service: services.RedisService,
        scheduler_service: services.SchedulerService,
    ) -> typing.Optional[schemas.HabitRead]:
        """Удаляет привычку."""

        habit_id = int(callback_query.data.split(sep=":")[-1])
        token = await redis_service.get_token(telegram_id=callback_query.from_user.id)
        if not token:
            await self.wizard.goto(app_scenes.MainMenuScene)

        habit = await api_service.delete_habit(
            token, cmd=schemas.HabitDeleteCommand(id=habit_id)
        )
        if habit is not None:
            await callback_query.message.edit_text(
                text=f"Привычка '{habit.title}' удалена ❎"
            )
            # TODO: реализовать удаление задачи из scheduler
        await self.wizard.goto(app_scenes.MainMenuScene)
