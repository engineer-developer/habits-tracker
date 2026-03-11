from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import (
    CallbackQuery,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from tg_bot.callbacks.user_profile import ProfileAction, ProfileMenuCallback
from tg_bot.configs.loguru_config import logger
from tg_bot.keyboards.kb_factory import kb_profile

__all__ = (
    # all scenes
    "MainMenuScene",
    "HabitListScene",
    "HabitEditScene",
)


BUTTON_CANCEL = KeyboardButton(text="Cancel")
BUTTON_BACK = KeyboardButton(text="Back")


class CancellableScene(Scene):
    """
    This scene is used to handle cancel and back buttons,
    can be used as a base class for other scenes that needs to support cancel and back buttons.
    """

    @on.message(F.text.upper() == BUTTON_CANCEL.text.upper())
    async def handle_cancel(self, message: Message) -> None:
        await self.wizard.exit()

    @on.message(F.text.upper() == BUTTON_BACK.text.upper())
    async def handle_back(self, message: Message) -> None:
        await self.wizard.back()


class HabitEditScene(CancellableScene, state="menu_habit_edit"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        logger.debug(f"{await self.wizard.state.get_state()}")
        await message.answer(text="Habit_edit", reply_markup=ReplyKeyboardRemove())

    @on.message(F.text.not_in([BUTTON_BACK.text, BUTTON_CANCEL.text]))
    async def choose_button(self, message: Message):
        await message.answer(
            text="Choose button bellow",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[BUTTON_BACK, BUTTON_CANCEL]],
                resize_keyboard=True,
            ),
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, cbq: CallbackQuery):
        await cbq.answer()
        await self.on_enter(cbq.message)


class HabitListScene(CancellableScene, state="menu_habit_list"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        logger.debug(f"{await self.wizard.state.get_state()}")

        await message.answer(
            text="Habit_list",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="edit_habit"),
                        BUTTON_BACK,
                        BUTTON_CANCEL,
                    ]
                ],
                resize_keyboard=True,
            ),
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, cbq: CallbackQuery):
        await cbq.answer()
        await self.on_enter(cbq.message)

    @on.message(F.text == "edit_habit")
    async def goto_edit_habit(self, message: Message):
        await self.wizard.goto(HabitEditScene)


class MainMenuScene(
    Scene,
    reset_data_on_enter=True,
    reset_history_on_enter=True,
    callback_query_without_state=True,
):
    @on.message.enter()
    # @on.message(Command("menu"))
    async def on_enter(self, message: Message):
        logger.debug(f"{await self.wizard.state.get_state()}")
        hide_keyboard_message = await message.answer(
            text="Обновляем интерфейс...", reply_markup=ReplyKeyboardRemove()
        )
        await hide_keyboard_message.delete()
        await message.answer(text="Text", reply_markup=kb_profile())

    @on.callback_query(
        ProfileMenuCallback.filter(F.action == ProfileAction.habits_list)
    )
    async def goto_habits_list(self, cbq: CallbackQuery):
        await cbq.answer()
        await self.wizard.goto(HabitListScene)
