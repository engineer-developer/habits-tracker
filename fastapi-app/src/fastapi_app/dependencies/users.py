from typing import Annotated

from containers.app_container import AppContainer
from dependency_injector.wiring import Provide
from fastapi import Depends
from services import UserService

DepsUserService = Annotated[UserService, Depends(Provide[AppContainer.user_service])]
