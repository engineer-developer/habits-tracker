from aiogram.dispatcher.router import Router
from aiogram.filters.command import CommandStart

from tg_bot import scenes

router = Router()
router.message.register(scenes.MainMenuScene.as_handler(), CommandStart())
