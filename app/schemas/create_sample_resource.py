from uuid import UUID

from .sample_resource_common import SampleResourceBase, to_lower_camel_case
from .mongo_model import BaseModel
from pydantic import ConfigDict


class CreateSampleResourceReq(SampleResourceBase):
    model_config = ConfigDict(alias_generator=to_lower_camel_case)


class CreateSampleResourceResp(BaseModel):
    id: UUID
