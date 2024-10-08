from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from repository.user import UserRepository
from repository import Storage
from repository.schemas import SessionType

from models.user import *
from models.auth import *

from hashlib import pbkdf2_hmac
from config import config
from utils.http import JWTHandler
from utils.session import UserSession
from utils.validate import ValidateInput

from re import match


class PasswordProcesser:
    def __init__(self, raw_pass: str, salt):
        self._raw = raw_pass
        self._salt = salt
        self._ITERATIONS = 10000

    def hash(self):
        return pbkdf2_hmac(
            "sha256",
            self._raw.encode("utf-8"),
            self._salt.encode("utf-8"),
            self._ITERATIONS,
        ).hex()

    def verify(self, hashed_pass: str):
        return self.hash() == hashed_pass


class AuthService:
    def __init__(
        self,
        repo: UserRepository = Depends(UserRepository),
        storage: Storage = Depends(Storage),
        user_sess: UserSession = Depends(UserSession),
    ):
        self._repo = repo
        self._jwt = JWTHandler(storage._fstore)
        self._user_sess = user_sess

    async def create(self, newUser: CreateUserModel) -> dict[str, str]:
        existUser = await self._repo.get(QueryUserModel(email=newUser.email))
        if existUser:
            raise HTTPException(status_code=409, detail="User already exists")
        newUser.password = PasswordProcesser(newUser.password, config["SALT"]).hash()
        user = await self._repo.add(newUser)
        return jsonable_encoder(
            GetUserDetail.model_validate(user, strict=False, from_attributes=True)
        )

    async def gen_token(self, authInfo: UserAuth) -> dict[str, str]:
        if match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            authInfo.identity,
        ):
            query = QueryUserModel(email=authInfo.identity)
        else:
            query = QueryUserModel(username=authInfo.identity)
        existUser = await self._repo.get(query)
        if not existUser:
            raise HTTPException(status_code=404, detail="User does not exist")
        access_token = self._jwt.create_token({"id": str(existUser.id)})
        self._user_sess.attach(existUser, access_token)
        self._user_sess.log(SessionType.NEW)
        return AccessResponse(access_token=access_token).model_dump()

    async def verify(self, token: str) -> dict[str, bool]:
        return IsValidToken(is_valid=self._jwt.verify(token) is not None).model_dump()

    async def get(self, id: str) -> dict[str, str]:
        try:
            user = await self._repo.get(QueryUserModel(id=id))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        if not user:
            raise HTTPException(status_code=404, detail="User does not exist")
        return jsonable_encoder(
            GetUserDetail.model_validate(user, strict=False, from_attributes=True)
        )

    async def update(self, id: str, userInfo: UpdateUserModel) -> dict[str, str]:
        try:
            user = await self._repo.update(id, userInfo)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return jsonable_encoder(
            GetUserDetail.model_validate(user, strict=False, from_attributes=True)
        )
    
    async def get_keys(self, subject: str) -> dict[str, str]:
        if ValidateInput.is_email(subject):
            own_resource = subject == self._user_sess._user.email
            user = await self._repo.get(QueryUserModel(email=subject))
        elif subject == "me":
            own_resource = True
            user = self._user_sess._user
        else:
            own_resource = subject == self._user_sess._user.username
            user = await self._repo.get(QueryUserModel(username=subject))
        if not user:
            raise HTTPException(status_code=404, detail="User does not exist")
        if own_resource:
            keys = CrytoKey(public_key=user.key.public_key, enc_pri=user.key.enc_pri).model_dump()
        else:
            keys = CrytoKey(public_key=user.key.public_key).model_dump()
        return keys