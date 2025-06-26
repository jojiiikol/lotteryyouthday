from enum import Enum

from pydantic import BaseModel

class SexEnum(Enum):
    male = 'male'
    female = 'female'

class UserSchema(BaseModel):
    id: int
    tg_id: int
    name: str
    last_name: str
    sex: SexEnum
    is_winner: bool

    class Config:
        from_attributes = True

class CreateUserSchema(BaseModel):
    name: str
    tg_id: int
    last_name: str
    sex: SexEnum
    is_winner: bool = False

class UpdateUserSchema(BaseModel):
    is_winner: bool = None

class TgIdUserSchema(BaseModel):
    tg_id: int