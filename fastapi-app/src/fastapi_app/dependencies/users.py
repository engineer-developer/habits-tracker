from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from fastapi_app.containers.app_container import AppContainer
from fastapi_app.services.users import UserService

DepsUserService = Annotated[UserService, Depends(Provide[AppContainer.user_service])]
