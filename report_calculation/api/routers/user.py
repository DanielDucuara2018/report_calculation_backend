from fastapi import APIRouter

from report_calculation.actions.user import create, delete, read, update
from report_calculation.schema import UserRequest as SchemaUserRequest
from report_calculation.schema import UserResponse as SchemaUserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

## Users
# add new user in database
@router.post("/")
async def create_user(user: SchemaUserRequest) -> SchemaUserResponse:
    return create(user)


# get crypto data
@router.get("/{user_id}")
async def read_user(user_id: str) -> SchemaUserResponse:
    return read(user_id)


@router.get("/")
async def read_user() -> list[SchemaUserResponse]:
    return read()


# update crypto data
@router.put("/{user_id}")
async def update_user(user_id: str, data: SchemaUserRequest) -> SchemaUserResponse:
    return update(user_id, data)


# delete existing from db
@router.delete("/{user_id}")
async def delete_currency(user_id: str) -> SchemaUserResponse:
    return delete(user_id)
