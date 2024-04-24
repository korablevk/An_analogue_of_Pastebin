from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    name: str
    email: EmailStr
    password: str