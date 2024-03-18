from typing import Optional

from fastapi import APIRouter, Depends

from report_calculation.actions.purchase import create, delete, read, update
from report_calculation.actions.user import get_current_user
from report_calculation.schema import PurchaseRequest, PurchaseResponse, UserResponse

router = APIRouter(
    prefix="/purchases",
    tags=["purchases"],
    responses={404: {"description": "Not found"}},
)

## Purchases
# add new purchase in database
@router.post("/")
async def add_purchase(
    purchase_info: PurchaseRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> PurchaseResponse:
    return create(current_user.user_id, purchase_info)


# get purchase data
@router.get("/")
async def read_purchase(
    purchase_id: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_user),
) -> list[PurchaseResponse]:
    if purchase_id:
        return read(current_user.user_id, purchase_id)
    return read(current_user.user_id)


# update purchase data
@router.put("/")
async def update_purchase(
    purchase_id: str,
    purchase: PurchaseRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> PurchaseResponse:
    return update(current_user.user_id, purchase_id, purchase)


# delete purchase from db
@router.delete("/")
async def delete_purchase(
    purchase_id: str, current_user: UserResponse = Depends(get_current_user)
) -> PurchaseResponse:
    return delete(current_user.user_id, purchase_id)
