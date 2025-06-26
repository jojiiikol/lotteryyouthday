from sqlalchemy import select

from config import new_session
from model.user import UserModel
from schema.user import CreateUserSchema, UpdateUserSchema


class UserRepository():
    async def get_all(self):
        async with new_session() as session:
            query = select(UserModel)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_not_winners(self):
        async with new_session() as session:
            query = select(UserModel).where(UserModel.is_winner == False)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_one_by_tg_id(self, tg_id: int):
        async with new_session() as session:
            query = select(UserModel).where(UserModel.tg_id == tg_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create(self, user_data: CreateUserSchema):
        async with new_session() as session:
            user = UserModel(**user_data.dict())
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def update(self, user_id: int, user_data: UpdateUserSchema):
        async with new_session() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one()

            for field, value in user_data.dict(exclude_unset=True).items():
                setattr(user, field, value)

            await session.commit()
            await session.refresh(user)

            return user