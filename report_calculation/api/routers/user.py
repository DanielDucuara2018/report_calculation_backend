from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from report_calculation.actions.user import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create,
    create_access_token,
    delete,
    get_current_user,
    read,
    update,
)
from report_calculation.schema import Token, UserRequest, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

## Users
## get token
@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


# add new user in database
@router.post("/")
async def create_user(user: UserRequest) -> UserResponse:
    return create(user)


# get user data
@router.get("/me", response_model=UserResponse)
async def read_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return current_user


@router.get("/")
async def read_users() -> list[UserResponse]:
    return read()


# update user data
@router.put("/")
async def update_user(
    data: UserRequest, current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    return update(current_user.user_id, data)


# delete existing user from db
@router.delete("/")
async def delete_currency(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return delete(current_user.user_id)
