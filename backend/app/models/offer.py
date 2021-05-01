from typing import Optional
from enum import Enum

from uuid import UUID, uuid4

from pydantic import Field

from app.models.core import DateTimeModelMixin, CoreModel
from app.models.user import UserPublic
from app.models.cleaning import CleaningPublic


class OfferStatus(str, Enum):
    accepted = "accepted"
    rejected = "rejected"
    pending = "pending"
    cancelled = "cancelled"
    completed = "completed"


class OfferBase(CoreModel):
    user_id: Optional[UUID]
    cleaning_id: Optional[UUID]
    status: Optional[OfferStatus] = OfferStatus.pending


class OfferCreate(OfferBase):
    user_id: UUID = Field(default_factory=uuid4)
    cleaning_id: UUID = Field(default_factory=uuid4)


class OfferUpdate(CoreModel):
    status: OfferStatus


class OfferInDB(DateTimeModelMixin, OfferBase):
    user_id: UUID = Field(default_factory=uuid4)
    cleaning_id: UUID = Field(default_factory=uuid4)


class OfferPublic(OfferInDB):
    user: Optional[UserPublic]
    cleaning: Optional[CleaningPublic]
