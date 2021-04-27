from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """
    pass


class IDModelMixin(BaseModel):
    id: UUID = Field(default_factory=uuid4)
