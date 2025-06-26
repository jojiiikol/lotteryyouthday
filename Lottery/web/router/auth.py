from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response

from auth_service import AuthService

router = APIRouter()

@router.post("/token")
async def login(auth_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthService = Depends()):
    token = await service.login(auth_data)
    return token