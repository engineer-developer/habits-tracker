"""Модуль представлений привычек."""

from fastapi.routing import APIRouter

router = APIRouter(prefix="/habits", tags=["habits"])

#
# @router.post(
#     "/",
#     description="Добавление новой привычки",
#     response_model=habits_schema.HabitOutDto,
# )
# async def add_habit(
#     habit_data: habits_schema.HabitAddDto,
#     user: GetCurrentActiveUser,
#     session: CommonAsyncSession,
# ) -> models.habits.Habit:
#     """Представление для добавления привычки."""
#     habit = await habits.add_habit_to_db(
#         habit_data=habit_data.model_dump(),
#         user_id=user.id,
#         session=session,
#     )
#
#     if habit is None:
#         raise HTTPException(status_code=400, detail="Ошибка добавления привычки.")
#
#     logger.debug("Добавлена привычка '{}'.", habit)
#     await session.refresh(habit, ["tracking"])
#     return habit

#
# @router.get(
#     "/",
#     description="Получение всех привычек пользователя.",
#     response_model=list[habits.HabitOutDto],
# )
# async def get_all_users_habits(
#     user: GetCurrentActiveUser,
#     session: CommonAsyncSession,
#     completed: Annotated[bool, Query(description="Показ завершенных привычек")] = False,
# ) -> list[habits.HabitOutDto]:
#     """Представление для получения всех привычек пользователя."""
#     habits_orm = await habit_service.fetch_all_habit_by_user_id(
#         user_id=user.id,
#         session=session,
#         completed=completed,
#     )
#
#     if not habits_orm:
#         error_msg = "Привычек не найдено."
#         logger.error(error_msg)
#         raise HTTPException(status_code=404, detail=error_msg)
#
#     habits_dto = [habits.HabitOutDto.model_validate(habit) for habit in habits_orm]
#     return habits_dto
#
#
# @router.get(
#     "/{id:int}/",
#     description="Получение привычки по id.",
#     response_model=habits.HabitOutDto,
# )
# async def get_habit_by_id(
#     id: Annotated[int, Path()],
#     user: GetCurrentActiveUser,
#     session: CommonAsyncSession,
# ) -> models.habits.Habit:
#     """Представление для получения привычки по id."""
#     habit = await habit_service.fetch_habit_by_id(id=id, session=session)
#     if not habit:
#         error_msg = f"Привычки c id={id} не найдено."
#         logger.error(error_msg)
#         raise HTTPException(status_code=404, detail=error_msg)
#
#     return habit
#
#
# @router.patch(
#     "/{id:int}/",
#     description="Изменение привычки",
#     response_model=habits.HabitOutDto,
# )
# async def modify_habit_data(
#     id: Annotated[int, Path()],
#     habit_data: habits.HabitPatchDto,
#     user: GetCurrentActiveUser,
#     session: CommonAsyncSession,
# ) -> models.habits.Habit:
#     """Представление для изменения привычки."""
#
#     habit, edited = await habit_service.edit_habit(
#         id=id,
#         data=habit_data.model_dump(),
#         session=session,
#     )
#     if habit is None:
#         error_msg = f"Привычки c id={id} не найдено."
#         logger.error(error_msg)
#         raise HTTPException(status_code=404, detail=error_msg)
#
#     if edited:
#         logger.debug("Данные привычки {} изменены.", habit)
#
#     return habit
#
#
# @router.delete(
#     "/{id:int}/",
#     description="Удаление привычки",
#     response_model=habits.HabitDeleteInfoDto,
# )
# async def delete_habit(
#     id: Annotated[int, Path()],
#     user: GetCurrentActiveUser,
#     session: CommonAsyncSession,
# ) -> habits.HabitDeleteInfoDto:
#     """Представление для удаления привычки."""
#
#     deleted_habit_id = await habit_service.delete_habit(id=id, session=session)
#     if not deleted_habit_id:
#         error_msg = f"Привычки c id={id} не найдено."
#         logger.error(error_msg)
#         raise HTTPException(status_code=404, detail=error_msg)
#
#     return habits.HabitDeleteInfoDto(habit_id=deleted_habit_id)
#
#
# @router.post(
#     "/confirm_execution/",
#     description="Регистрация выполнения привычки",
#     response_model=habits.HabitOutDto,
# )
# async def registering_habit_execution(
#     confirm_data: habits.HabitExecutionData,
#     user: GetCurrentActiveUser,
#     session: CommonAsyncSession,
# ) -> models.habits.Habit:
#     """Представление для регистрации выполнения привычки."""
#     habit = await habit_service.fetch_habit_by_id(
#         id=confirm_data.habit_id,
#         session=session,
#     )
#     if not habit:
#         error_msg = f"Привычки '{confirm_data.habit_id}' не найдено."
#         logger.error(error_msg)
#         raise HTTPException(status_code=404, detail=error_msg)
#
#     tracking = models.tracking.Tracking(execution_time=confirm_data.execution_time)
#     habit.tracking.append(tracking)
#     await session.commit()
#     logger.debug("Зарегистрировано выполнение привычки '{}'.", habit)
#
#     if habit.remind_quantity == len(habit.tracking):
#         habit.completed = True
#         await session.commit()
#         logger.debug("Привитие привычки '{}' завершено.", habit)
#
#     return habit
