from tg_bot.scenes.auth import LoginScene, RegisterScene
from tg_bot.scenes.common import CancellableScene
from tg_bot.scenes.habits import (
    ActiveHabitsScene,
    AddHabitConfirmScene,
    AddHabitDescriptionInputScene,
    AddHabitRemindQuantityInputScene,
    AddHabitRemindTimeInputScene,
    AddHabitTitleInputScene,
    CompletedHabitsScene,
    HabitDeleteScene,
    HabitDetailsScene,
    HabitEditScene,
    HabitMarkCompletedScene,
    HabitUpdateDescriptionScene,
    HabitUpdateRemindQuantityScene,
    HabitUpdateRemindTimeScene,
    HabitUpdateTitleScene,
)
from tg_bot.scenes.main_menu import MainMenuScene


__all__ = (
    "scenes",
    "CancellableScene",
    "MainMenuScene",
    "LoginScene",
    "RegisterScene",
    "ActiveHabitsScene",
    "CompletedHabitsScene",
    "HabitDetailsScene",
    "HabitMarkCompletedScene",
    "HabitDeleteScene",
    "HabitEditScene",
    "HabitUpdateTitleScene",
    "HabitUpdateDescriptionScene",
    "HabitUpdateRemindTimeScene",
    "HabitUpdateRemindQuantityScene",
    "AddHabitTitleInputScene",
    "AddHabitDescriptionInputScene",
    "AddHabitRemindTimeInputScene",
    "AddHabitRemindQuantityInputScene",
    "AddHabitConfirmScene",
)


scenes = [
    MainMenuScene,
    LoginScene,
    RegisterScene,
    ActiveHabitsScene,
    CompletedHabitsScene,
    HabitDetailsScene,
    HabitMarkCompletedScene,
    HabitDeleteScene,
    HabitEditScene,
    HabitUpdateTitleScene,
    HabitUpdateDescriptionScene,
    HabitUpdateRemindTimeScene,
    HabitUpdateRemindQuantityScene,
    AddHabitTitleInputScene,
    AddHabitDescriptionInputScene,
    AddHabitRemindTimeInputScene,
    AddHabitRemindQuantityInputScene,
    AddHabitConfirmScene,
]
