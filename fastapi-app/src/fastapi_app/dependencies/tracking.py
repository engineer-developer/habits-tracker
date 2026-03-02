from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi import Depends

from fastapi_app.containers.app_container import AppContainer
from fastapi_app.services.tracking import TrackingService

DepsTrackingService = Annotated[
    TrackingService,
    Depends(Provide[AppContainer.tracking_service]),
]
