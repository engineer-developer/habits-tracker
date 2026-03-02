from fastapi_app.repositories.tracking import TrackingRepository
from fastapi_app.schemas.habits import HabitByIdQuery
from fastapi_app.schemas.tracking import TrackingCreateCommand, TrackingRead
from fastapi_app.services.habits import HabitService


class TrackingService:
    """Сервис отслеживания привычек."""

    def __init__(
        self,
        repository: TrackingRepository,
        habit_service: HabitService,
    ) -> None:
        self.repository = repository
        self.habit_service = habit_service

    async def add_tracking(self, cmd: TrackingCreateCommand) -> TrackingRead:
        """Добавляет отслеживание привычки."""
        tracking = await self.repository.create(cmd)
        await self.habit_service.mark_habit_as_completed(
            query=HabitByIdQuery(id=cmd.habit_id)
        )
        return tracking
