from typing import TypeVar

import pydantic

__all__ = ("BaseDtoModel", "Model")

Model = TypeVar("Model", bound="BaseDtoModel")


class BaseDtoModel(pydantic.BaseModel):
    """Базовая модель для всех схем в проекте."""
