from aiogram import F
from aiogram.fsm.scene import Scene, on, After
from aiogram.types import CallbackQuery


class CancellableScene(Scene):
    """
    This scene is used to handle cancel and back buttons,
    can be used as a base class for other scenes that needs to support cancel and back buttons.
    """

    @on.callback_query(F.data == "back", after=After.back())
    async def handle_back(self, callback_query: CallbackQuery) -> None:
        await callback_query.answer()

    @on.callback_query(F.data == "cancel", after=After.exit())
    async def handle_cancel(self, callback_query: CallbackQuery) -> None:
        await callback_query.answer()
        await callback_query.message.edit_text("Нажмите /start")
