from sqlalchemy import Integer, String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from model.base import BaseModel
from schema.user import SexEnum


class UserModel(BaseModel):
    __tablename__ = 'participant'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    sex: Mapped[SexEnum | None] = mapped_column(default=None, nullable=True)
    is_winner: Mapped[bool] = mapped_column(Boolean, default=False)