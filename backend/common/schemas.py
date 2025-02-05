from datetime import datetime
from enum import Enum
from typing import Any

from config import TIMEZONE
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.astimezone(TIMEZONE).isoformat(timespec='seconds')


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(extra='forbid', json_encoders={
        datetime: convert_datetime_to_iso_8601_with_z_suffix
    })


class IgnoreCaseEnum(str, Enum):
    @classmethod
    def _missing_(cls, value: str):
        if value.lower() in cls:
            return value.lower()

class CustomStr(str):
    @classmethod
    def validate(cls, value):
        return value

    def __new__(cls, value):
        return cls.validate(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))
