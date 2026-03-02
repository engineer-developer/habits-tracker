from dependency_injector.wiring import inject

from fastapi import APIRouter, status

from fastapi_app.dependencies.tracking import DepsTrackingService
from fastapi_app.schemas.tracking import TrackingRead, TrackingCreateCommand


router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=TrackingRead,
)
@inject
async def add_habit_tracking(
    cmd: TrackingCreateCommand,
    tracking_service: DepsTrackingService,
) -> TrackingRead:
    """Роут для добавления отслеживания привычки."""
    tracking = await tracking_service.add_tracking(cmd)
    return tracking
