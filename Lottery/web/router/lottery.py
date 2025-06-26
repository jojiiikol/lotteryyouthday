import random
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException

from dep import get_current_user
from repository.user_repository import UserRepository
from schema.user import UserSchema, UpdateUserSchema

router = APIRouter(
    tags=['lottery'],
    prefix='/lottery'
)



@router.post("/")
async def lottery(repository=Depends(UserRepository), current_user: UserSchema = Depends(get_current_user)) -> Dict[str, List[UserSchema] | UserSchema]:
    users = await repository.get_not_winners()
    users = [UserSchema.from_orm(user) for user in users]
    if len(users) == 0:
        raise HTTPException(status_code=404, detail="No winners")
    winner = random.choice(users)
    winner = await repository.update(winner.id, UpdateUserSchema(is_winner=True))
    return ({"users": users,
             "winner": winner})

@router.get("/get_users")
async def get_users(repository=Depends(UserRepository), current_user: UserSchema = Depends(get_current_user)):
    users = await repository.get_all()
    users = [UserSchema.from_orm(user) for user in users]
    return ({"users": users})