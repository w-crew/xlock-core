from fastapi import APIRouter, Depends
from services.auth import AuthService
from models.user import *
from models.auth import *

from utils.http import *
from utils.session import *
from utils.validate import *

authRouter = APIRouter(tags=["Auth"])


@authRouter.post("/register", response_model=UserDetailResponse)
async def register_user(
    newUserInfo: CreateUserModel,
    service: AuthService = Depends(AuthService),
):
    new_user = await service.create(newUserInfo)
    return APIResponse.as_json(201, "User created successfully", new_user)


@authRouter.post("/login", response_model=UserAuthResponse)
async def login_user(
    authInfo: UserAuth,
    service: AuthService = Depends(AuthService),
):
    result = await service.gen_token(authInfo)

    res = APIResponse.as_json(200, "User logged in successfully", result)
    res.set_cookie(
        "auth", result["access_token"], httponly=True, samesite="strict", path="/"
    )
    return res


@authRouter.post("/verify", response_model=VerifyTokenResponse)
async def verify_token(
    tokenInfo: VerifyTokenRequest,
    service: AuthService = Depends(AuthService),
):
    result = await service.verify(tokenInfo.access_token)

    return APIResponse.as_json(200, "Token verified", result)


@authRouter.get("/me", response_model=UserDetailResponse)
async def get_user(
    service: AuthService = Depends(AuthService),
    session: UserSession = Depends(UserSession),
):
    user = session.get_authorized_user()
    if not user:
        return APIResponse.as_json(401, "Unauthorized", None)
    user = await service.get(user.id)
    return APIResponse.as_json(200, "OK", user)


@authRouter.patch("/user", response_model=UserDetailResponse)
async def update_user(
    userInfo: UpdateUserModel,
    service: AuthService = Depends(AuthService),
    session: UserSession = Depends(UserSession),
):
    user = session.get_authorized_user()
    if not user:
        return APIResponse.as_json(401, "Unauthorized", None)
    user = await service.update(user.id, userInfo)
    return APIResponse.as_json(200, "User updated successfully", user)

@authRouter.get("/keys/{subject}", response_model=CrytoKeyResponse)
async def get_keys(
    subject: str,
    service: AuthService = Depends(AuthService),
    user_session: UserSession = Depends(UserSession),
):
    caller = user_session.get_authorized_user()
    if not caller:
        return APIResponse.as_json(401, "Unauthorized", None)
    # if ValidateInput.is_email(subject):
    #     own_resource = subject == caller.email
    # elif subject == "me":
    #     own_resource = True
    #     subject = caller.id
    # else:
    #     own_resource = subject == caller.username
    keys = await service.get_keys(subject)
    return APIResponse.as_json(200, "OK", keys)