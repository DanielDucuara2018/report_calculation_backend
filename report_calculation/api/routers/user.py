from fastapi import APIRouter

from report_calculation.actions.user import create, delete, read, update
from report_calculation.schema import UserRequest, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

## Users
# add new user in database
@router.post("/")
async def create_user(user: UserRequest) -> UserResponse:
    return create(user)


# get crypto data
@router.get("/{user_id}")
async def read_user(user_id: str) -> UserResponse:
    return read(user_id)


@router.get("/")
async def read_user() -> list[UserResponse]:
    return read()


# update crypto data
@router.put("/{user_id}")
async def update_user(user_id: str, data: UserRequest) -> UserResponse:
    return update(user_id, data)


# delete existing from db
@router.delete("/{user_id}")
async def delete_currency(user_id: str) -> UserResponse:
    return delete(user_id)
