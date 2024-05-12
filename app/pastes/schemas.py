from enum import Enum
from pydantic import BaseModel, EmailStr
from fastapi import Form


class VisibilityEnum(Enum):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'


# @form_body
class SPastes(BaseModel):
    comment: str
    visibility: VisibilityEnum
    expiration: int


