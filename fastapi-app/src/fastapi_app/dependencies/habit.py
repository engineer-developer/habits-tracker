from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from fastapi_app.containers.app_container import AppContainer
from fastapi_app.services.habits import HabitService

DepsHabitService = Annotated[
    HabitService,
    Depends(Provide[AppContainer.habit_service]),
]
