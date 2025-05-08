from pydantic import StringConstraints, Field
from datetime import datetime
from uuid import UUID

from .mongo_model import MongoModel
from typing_extensions import Annotated


def to_lower_camel_case(string: str) -> str:
    split_str = string.split('_')
    return split_str[0] + ''.join(word.capitalize() for word in split_str[1:])


class SampleResourceBase(MongoModel):
    name: Annotated[str, StringConstraints(max_length=255)]


class SampleResource(SampleResourceBase):
    model_config = {
        "populate_by_name": True
    }
    id: UUID = Field(alias="_id")
    create_time: datetime
    update_time: datetime
    deleted: bool
