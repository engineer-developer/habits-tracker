from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, status

from fastapi_app.dependencies.auth import get_current_user_telegram_id
from fastapi_app.dependencies.tracking import DepsTrackingService
from fastapi_app.schemas.tracking import TrackingCreateCommand, TrackingRead

router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=TrackingRead,
    dependencies=[Depends(get_current_user_telegram_id)],
)
@inject
async def add_habit_tracking(
    cmd: TrackingCreateCommand,
    tracking_service: DepsTrackingService,
) -> TrackingRead:
    """Роут для добавления отслеживания привычки."""
    tracking = await tracking_service.add_tracking(cmd)
    return tracking
