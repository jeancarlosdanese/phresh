from typing import Optional

from pydantic import EmailStr, HttpUrl, Field, constr, validator
from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel

from uuid import UUID, uuid4


class ProfileBase(CoreModel):
    full_name: Optional[constr(strip_whitespace=True, max_length=140)]
    phone_number: Optional[constr(strip_whitespace=True, max_length=50)]
    bio: Optional[str]
    image: Optional[HttpUrl]


class ProfileCreate(ProfileBase):
    """
    The only field required to create a profile is the users id
    """
    user_id: UUID = Field(default_factory=uuid4)


class ProfileUpdate(ProfileBase):
    """
    Allow users to update any or no fields, as long as it's not user_id
    """
    pass


class ProfileInDB(IDModelMixin, DateTimeModelMixin, ProfileBase):
    user_id: UUID = Field(default_factory=uuid4)
    username: Optional[str]
    email: Optional[EmailStr]


class ProfilePublic(ProfileInDB):
    pass
