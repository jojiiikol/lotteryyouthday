from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from passlib.context import CryptContext

from repository.user_repository import UserRepository
from schema.auth import AuthDataSchema, TokenSchema
from schema.user import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token_dep = Annotated[str, Depends(oauth2_scheme)]
ADMIN_LOGIN = "jojiiikol"
ADMIN_PASSWORD = "<PASSWORD>"

class AuthService:
    TOKEN_LIFETIME = timedelta(minutes=120)
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    def __init__(self, repository: UserRepository = Depends()):
        self.repository = repository

    async def login(self, auth_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenSchema:
        auth_data = AuthDataSchema(username=auth_data.username, password=auth_data.password)
        await self.authenticate(auth_data)
        token = self.create_token()
        return token

    async def get_current_user(self, token: str = Depends(token_dep)):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms='HS256')
            username = payload['sub']
            if username is None:
                raise HTTPException(status_code=401, detail='Token expired')
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
        return True

    async def authenticate(self, auth_data: AuthDataSchema):
        if auth_data.username != "jojiiikol":
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        hashed_password = pwd_context.hash(ADMIN_PASSWORD)
        if not self.verify_password(auth_data.password, hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

    def verify_password(self, password: str, user_password: str) -> bool:
        return pwd_context.verify(password, user_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_token(self) -> TokenSchema:
        token_data = {"sub": ADMIN_LOGIN,
                      "exp": datetime.now(timezone.utc) + self.TOKEN_LIFETIME}
        token = jwt.encode(token_data, self.SECRET_KEY, algorithm='HS256')
        return TokenSchema(access_token=token, token_type='Bearer')
