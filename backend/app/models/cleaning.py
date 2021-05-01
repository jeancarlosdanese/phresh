from typing import Optional, Union
from enum import Enum
from uuid import UUID

from pydantic import constr

from app.models.core import IDModelMixin, DateTimeModelMixin, CoreModel
from app.models.user import UserPublic


class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class CleaningBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    name: Optional[constr(strip_whitespace=True, max_length=140)]
    description: Optional[constr(strip_whitespace=True, max_length=254)]
    price: Optional[float]
    cleaning_type: Optional[CleaningType] = "spot_clean"


class CleaningCreate(CleaningBase):
    name: str
    price: float


class CleaningUpdate(CleaningBase):
    cleaning_type: Optional[CleaningType]


class CleaningInDB(IDModelMixin, DateTimeModelMixin, CleaningBase):
    name: str
    price: float
    cleaning_type: CleaningType
    owner: UUID


class CleaningPublic(CleaningInDB):
    owner: Union[UUID, UserPublic]
