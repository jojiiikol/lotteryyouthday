from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from auth_service import AuthService
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

token_dep = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(token: token_dep, auth: AuthService = Depends(AuthService)):
    return await auth.get_current_user(token=token)