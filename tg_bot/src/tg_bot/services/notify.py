from dataclasses import dataclass

from pydantic import ValidationError

from tg_bot.api_requests.utils import get_habit_info
from tg_bot.core.bot_factory import bot
from tg_bot.services.logging_services import logger
from tg_bot.core.redis_factory import save_user_data
from tg_bot.keyboards.kb_factory import kb_confirm_habit_completed
from tg_bot.schemas.habit_schema import HabitJobDataDto





# def send_notice(**kwargs):
#     """Отправляем напоминание о привычке."""
#     try:
#         habit_job_data = HabitJobDataDto(**kwargs)
#         logger.debug("Данные из job: {}", habit_job_data.model_dump())
#     except ValidationError as exc:
#         logger.error(exc.errors())
#         return
#
#     user_id = habit_job_data.user_id
#     name = habit_job_data.name
#
#     habit_info: dict = get_habit_info(user_id=user_id, name=name)
#     if not habit_info:
#         logger.error("Данные о привычке не получены из бэкэнда.")
#         return
#
#     left_remind_quantity = calculate_left_remind_quantity(habit_info)
#     if left_remind_quantity and left_remind_quantity > 0:
#         msg_text = (
#             f"Напоминание о привычке: *{name}*\n"
#             f"Описание: *{habit_job_data.description}*\n"
#             f"Время выполнения: *{habit_job_data.remind_time}*\n"
#             f"Осталось выполнить: *{left_remind_quantity}*"
#         )
#
#         bot.send_message(
#             chat_id=habit_job_data.chat_id,
#             text=msg_text,
#             reply_markup=kb_confirm_habit_completed(),
#             parse_mode="Markdown",
#         )
#         save_user_data(user_id, "habit_name", name)


