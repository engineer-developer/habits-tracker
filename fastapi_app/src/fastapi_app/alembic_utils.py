"""Модуль взаимодействия с alembic."""

import shlex
from subprocess import Popen


def upgrade_to_head() -> None:
    """Функция запускает поток выполнения команды обновления базы данных."""
    alembic_upgrade_command = "alembic upgrade head"
    tokenized_command = shlex.split(alembic_upgrade_command)

    with Popen(tokenized_command) as proc:
        proc.wait()

    exit_code = proc.returncode

    if exit_code == 0:
        print("Alembic upgrade too head successful.")
    else:
        print("Alembic upgrade error.")
